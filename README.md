# Nitro CLI

CLI client for `judge.nitro-ai.org`.

## Features

- login using `cf_clearance` plus Nitro credentials
- list contests with page controls
- list tasks for a contest
- view full task statements
- submit solutions and wait for feedback
- list submissions
- inspect submission feedback/details
- interactive shell mode when run without arguments

## Requirements

- Python 3.10+

## Login

Nitro login still requires a valid `cf_clearance` cookie for `judge.nitro-ai.org`.

`nitro-cli` will use, in order:

1. `--cf-clearance`
2. `NITRO_CF_CLEARANCE`
3. the saved value from `~/.nitro-cli/state.json`
4. an interactive prompt

Example:

```bash
nitro-cli login --username MihneaStoica --password '...' --cf-clearance '...'
```

Or:

```bash
export NITRO_CF_CLEARANCE='...'
nitro-cli login
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
login [username] [password] [cf_clearance]
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

Before publishing publicly, choose and add a license file.
