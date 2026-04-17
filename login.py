#!/usr/bin/env python3
"""
Nitro AI Judge — Login Script

Usage:
    python3 login.py
"""

import base64
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request as urllib_request
import urllib.error as urllib_error

BASE_URL = "https://judge.nitro-ai.org"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
STATE_FILE = "/tmp/judge-login-state.json"


def hash_password(password: str) -> str:
    """Hash: SHA-256 → binary → base64. Matches frontend crypto.subtle.digest."""
    return base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()


def get_browser_cookies() -> tuple[str | None, str | None]:
    """Extract cf_clearance and session Cookie from agent-browser."""
    r = os.popen("agent-browser cookies 2>&1").read()
    cf = session = None
    for line in r.split("\n"):
        if "cf_clearance=" in line:
            cf = line.strip().split("=", 1)[1]
        elif line.startswith("Cookie="):
            session = line.split("=", 1)[1]
    return cf, session


def save_state(cf: str, session_cookie: str, username: str = None):
    state = {
        "cookies": [
            {"name": "cf_clearance", "value": cf},
            {"name": "Cookie", "value": session_cookie},
        ],
        "username": username,
        "timestamp": time.time(),
    }
    try:
        decoded = json.loads(base64.b64decode(urllib.parse.unquote(session_cookie)))
        state["access_token"] = decoded.get("accessToken")
        state["refresh_token"] = decoded.get("refreshToken")
        state["role"] = decoded.get("role")
        state["username"] = decoded.get("username", username)
    except Exception:
        pass
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"  Saved to {STATE_FILE}")


def test_session(cf: str, session: str) -> bool:
    """Check if session cookie is still valid."""
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/profile/personal.data",
            headers={
                "User-Agent": UA,
                "Cookie": f"cf_clearance={cf}; Cookie={session}",
            },
        )
        resp = urllib.request.urlopen(req, timeout=10)
        body = resp.read().decode("utf-8", errors="replace")
        return '"username"' in body or '"firstName"' in body
    except urllib.error.HTTPError:
        return False
    except Exception:
        return False


def login(username: str, password: str, cf: str) -> dict:
    hashed_pw = hash_password(password)
    form_data = urllib.parse.urlencode(
        {
            "username": username,
            "password": hashed_pw,
        }
    ).encode("utf-8")

    result = {
        "success": False,
        "session_cookie": None,
        "http_code": None,
        "error": None,
    }

    try:
        req = urllib.request.Request(
            f"{BASE_URL}/login.data",
            data=form_data,
            headers={
                "User-Agent": UA,
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Cookie": f"cf_clearance={cf}",
                "Origin": BASE_URL,
                "Referer": f"{BASE_URL}/login",
            },
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=15)
        result["http_code"] = resp.status
        body = resp.read().decode("utf-8", errors="replace")

        # Extract session cookie from Set-Cookie header
        for part in resp.headers.get("Set-Cookie", "").split(","):
            for cookie in part.split(";"):
                cookie = cookie.strip()
                if cookie.startswith("Cookie="):
                    result["session_cookie"] = cookie.split("=", 1)[1]

        if '"redirect"' in body and '"status",302' in body:
            result["success"] = True

    except urllib_error.HTTPError as e:
        result["http_code"] = e.code
        try:
            body = e.read().decode("utf-8", errors="replace")
            if e.code == 403:
                result["error"] = "HTTP 403 — Cloudflare challenge failed or expired"
            elif e.code == 401:
                result["error"] = "HTTP 401 — Wrong credentials"
            elif e.code == 500:
                result["error"] = f"HTTP 500 — Server error: {body[:200]}"
            else:
                result["error"] = f"HTTP {e.code}: {body[:200]}"
        except Exception:
            result["error"] = f"HTTP {e.code}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    username = input("Username: ").strip()
    if not username:
        print("Aborted.")
        sys.exit(1)

    import getpass

    password = getpass.getpass("Password: ")
    if not password:
        print("Aborted.")
        sys.exit(1)

    print()

    # Step 1: Get cf_clearance from browser
    print("Step 1 — Getting Cloudflare clearance from browser...")
    cf, existing_session = get_browser_cookies()
    if not cf:
        print("✗ Failed: Could not get cf_clearance from agent-browser")
        print(
            "  Make sure agent-browser is running and connected to judge.nitro-ai.org"
        )
        sys.exit(1)
    print(f"✓ Got cf_clearance: {cf[:40]}...")

    # Step 2: Try existing session first
    if existing_session:
        print("\nStep 2 — Checking existing session...")
        if test_session(cf, existing_session):
            save_state(cf, existing_session)
            print("✓ Existing session is still valid!")
            return 0
        print("  Session expired or invalid — logging in fresh...")

    # Step 3: Login with credentials
    print(f"\nStep 3 — Logging in as '{username}'...")
    result = login(username, password, cf)

    print(f"\n{'=' * 50}")
    print(f"HTTP Code: {result.get('http_code')}")

    if result["success"] and result.get("session_cookie"):
        print("✓ Login SUCCEEDED")
        decoded = json.loads(
            base64.b64decode(urllib.parse.unquote(result["session_cookie"]))
        )
        user = decoded.get("username")
        role = decoded.get("role")
        print(f"  User: {user}")
        print(f"  Role: {role}")
        save_state(cf, result["session_cookie"], user)
    else:
        print("✗ Login FAILED")
        print(f"  Error: {result.get('error')}")
        print(f"{'=' * 50}")
        return 1

    print(f"{'=' * 50}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
