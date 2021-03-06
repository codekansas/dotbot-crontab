# dotbot-crontab

Crontab plugin for Dotbot.

## Installation

Add `dotbot-crontab` as a submodule of your dotfiles repository:

```bash
git submodule add git@github.com:codekansas/dotbot-crontab.git
```

Update `install` script to enable the `dotbot-crontab` plugin:

```bash

"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" \
    -d "${BASEDIR}" \
    -c "${CONFIG}" \
    --plugin-dir dotbot-crontab \
    "${@}"
```

## Usage

Adds a `crontab` directive, which can be configured as follows:

```yaml
- crontab:
  - time: 0 5 * * *
    command: brew update && brew upgrade
    platform: darwin                        # Optional
  - time: 0 5 * * *
    command: apt update && apt upgrade
    platform: linux                         # Optional
```

## Under the Hood

This is basically just a wrapper for [python-crontab][python-crontab]. Doing `./install` clears the existing DotBot-generated commands and refreshes with whatever is in your `install.conf.yaml` file.

[python-crontab]: https://pypi.org/project/python-crontab/
