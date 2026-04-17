# Nitro CLI

CLI client for `judge.nitro-ai.org`.

## Features

- login using browser Cloudflare/session cookies
- list contests with page controls
- list tasks for a contest
- view full task statements
- submit solutions and wait for feedback
- list submissions
- inspect submission feedback/details
- interactive shell mode when run without arguments

## Requirements

- Python 3.10+
- `agent-browser` available in PATH and already able to read cookies for `judge.nitro-ai.org`

## Usage

Install into `~/.local/bin/nitro-cli`:

```bash
./install.sh
```

The installer warns if `~/.local/bin` is not in your `PATH`.

Direct commands:

```bash
python3 nitro-cli.py login
python3 nitro-cli.py contests
python3 nitro-cli.py contests --page 2
python3 nitro-cli.py contests --all-pages
python3 nitro-cli.py tasks algolymp/algolymp-preojia-ix-x
python3 nitro-cli.py task algolymp/algolymp-preojia-ix-x 1
python3 nitro-cli.py submissions algolymp/algolymp-preojia-ix-x 1 --mode both
python3 nitro-cli.py submission 3a009d767bd5 --org algolymp --comp algolymp-preojia-ix-x --task-id 1
python3 nitro-cli.py submit algolymp/algolymp-preojia-ix-x 1 --output submission.csv --source solution.py --wait
```

Interactive shell:

```bash
python3 nitro-cli.py
```

Example shell session:

```text
contest list
contest list --page 2
contest list --all-pages
contest select 1
task list
task select 1
task show
task submit submission.csv solution.py --wait
task submissions list --mode both
task submissions show 1
```

Shell commands:

```text
help
exit | quit
login [username] [password]
status
contest list [--all] [--page N] [--page-size N] [--all-pages]
contest select <index|org/slug>
contest show
task list
task select <index|id>
task show
task submit <output.csv> [source.py] [--note TEXT] [--wait]
task submissions list [--mode partial|complete|both]
task submissions show <index|short-id|full-id>
```

## State

Login state is stored in:

```text
~/.nitro-cli/state.json
```

Override with:

```bash
NITRO_STATE_DIR=/some/path python3 nitro-cli.py login
```

## Repo Notes

`competition-frontend/` and `competition-backend/` are not required for the published CLI.

Before publishing publicly, choose and add a license file.
