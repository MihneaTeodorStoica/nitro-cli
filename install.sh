#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SRC="$SCRIPT_DIR/nitro-cli.py"
DEST_DIR="$HOME/.local/bin"
DEST="$DEST_DIR/nitro-cli"

if [[ ! -f "$SRC" ]]; then
  printf 'error: missing source file: %s\n' "$SRC" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
install -m 755 "$SRC" "$DEST"

printf 'Installed %s\n' "$DEST"

case ":${PATH:-}:" in
  *":$DEST_DIR:"*) ;;
  *)
    printf '\nWarning: %s is not in PATH.\n' "$DEST_DIR" >&2
    printf 'Add this to your shell config:\n' >&2
    printf '  export PATH="$HOME/.local/bin:$PATH"\n' >&2
    ;;
esac
