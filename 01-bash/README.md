# 01-bash: development environment setup (slide 18)

## Part 1: shell

| Task | Command |
|---|---|
| Show the login shell | `echo $SHELL` → `/bin/zsh` |
| Install Oh My Zsh | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"` |
| Enable it and the Git plugin | add `export ZSH`, `ZSH_THEME="robbyrussell"`, `plugins=(git)` and `source $ZSH/oh-my-zsh.sh` to `~/.zshrc` |
| Reload the configuration | `source ~/.zshrc` |
| Test a Git alias | `gst` (= `git status`) |

## Part 2: Python

`python3 --version` → Python 3.13

## Part 3: `env_install.sh`

```bash
./env_install.sh
```

The script:
1. defines a `pretty_print` function (`printf` with blank lines around the message);
2. detects the OS with `$OSTYPE` (`macos`, `linux` or `unknown`);
3. checks `python3` with `command -v` and installs it with Homebrew if missing;
4. checks pip by running `python3 -m pip --version`, and installs it with `ensurepip` if missing;
5. installs Jupyter with the right package manager (`brew` on macOS, `apt` on Linux);
6. runs `brew doctor` on macOS.

## What I learned

- **Terminal vs shell**: the terminal is the window where you type; the shell (zsh, bash, sh) is the program that interprets the commands. Several shells can be installed.
- **Environment variables** hold values for the session, read with `$`: `$SHELL`, `$HOME`, `$USER`, `$OSTYPE`.
- **`source`** runs a file in the current shell, so changes to `~/.zshrc` apply without opening a new terminal.
- **Shebang** `#!/bin/bash`: tells the system which interpreter runs the script.
- **`chmod +x`** makes the script executable so it can be launched with `./env_install.sh`.
- **`command -v`** only checks that a command name exists; to test a command with options, run it in the `if` and check whether it succeeds.
- **`> /dev/null 2>&1`** hides the normal output and the errors.
- **`if [[ ... ]]; then ... elif ... else ... fi`**: every `if` is closed by `fi`.
