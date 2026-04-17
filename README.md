# Nitro CLI

CLI client for `judge.nitro-ai.org`.

## Features

- login using Playwright plus Nitro credentials
- list contests with page controls
- list tasks for a contest
- view full task statements
- submit solutions and wait for feedback
- list submissions
- inspect submission feedback/details
- interactive shell mode when run without arguments

## Requirements

- Python 3.10+
- Playwright is installed as a package dependency

## Login

`nitro-cli login` opens a real browser session using Playwright to obtain Cloudflare clearance, then completes the Nitro login flow automatically.

Behavior:

1. reuses saved session if still valid
2. reuses saved `cf_clearance` when possible
3. opens a browser if a fresh Cloudflare clearance is needed
4. retries login automatically if the saved clearance expired

On first use, `nitro-cli` may install the Playwright Chromium browser.

Browser behavior:

- headless by default, so no browser window flashes
- to force a visible browser for debugging:

```bash
NITRO_BROWSER_HEADLESS=0 nitro-cli login
```

Example:

```bash
nitro-cli login --username MihneaStoica --password '...'
```

## Installation

With `pipx`:

```bash
pipx install .
```

With `pip`:

```bash
python3 -m pip install .
```

For local development:

```bash
python3 -m pip install -e .
```

From PyPI:

```bash
pipx install nitro-cli
```

## Usage

Direct commands:

```bash
nitro-cli login
nitro-cli contests
nitro-cli contests --page 2
nitro-cli contests --all-pages
nitro-cli tasks algolymp/algolymp-preojia-ix-x
nitro-cli task algolymp/algolymp-preojia-ix-x 1
nitro-cli submissions algolymp/algolymp-preojia-ix-x 1 --mode both
nitro-cli submission 3a009d767bd5 --org algolymp --comp algolymp-preojia-ix-x --task-id 1
nitro-cli submit algolymp/algolymp-preojia-ix-x 1 --output submission.csv --source solution.py --wait
```

Interactive shell:

```bash
nitro-cli
```

Example shell session:

```text
contest list
contest list --page 2
contest list --all-pages
select 20
tasks
select 1
show
submit submission.csv solution.py --wait
submissions
submission 1
```

Shell commands:

```text
help
exit | quit
back
login [username] [password]
status
contests
contest list [--all] [--page N] [--page-size N] [--all-pages]
contest select <index|org/slug>
contest show
tasks
task list
task select <index|id>
select <index|id>
show
submit <output.csv> [source.py] [--note TEXT] [--wait]
task show
task submit <output.csv> [source.py] [--note TEXT] [--wait]
submissions [--mode partial|complete|both]
task submissions list [--mode partial|complete|both]
submission <index|short-id|full-id>
submission view <index|short-id|full-id>
task submissions show <index|short-id|full-id>
set-final <index|short-id|full-id>
unset-final <index|short-id|full-id>
```

## State

Login state is stored in:

```text
~/.nitro-cli/state.json
```

Override with:

```bash
NITRO_STATE_DIR=/some/path nitro-cli login
```

## Repo Notes

`competition-frontend/` and `competition-backend/` are not required for the published CLI.

## Publishing

This repo includes a GitHub Actions workflow at `.github/workflows/publish.yml`.

Behavior:

1. Builds the package on pushes, pull requests, and manual runs
2. Runs `twine check` on built distributions
3. Publishes to PyPI when you push a tag matching `v*`

Recommended release flow:

```bash
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine check dist/*
git tag v0.1.0
git push origin main --tags
```

For PyPI trusted publishing, configure PyPI to trust this GitHub repository and the `pypi` environment.

Before publishing publicly, choose and add a license file.
