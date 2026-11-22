# 02-git: Git mini exo (slide 26)

Repository built during the exercise: **[robinmoglia/my-first-repo](https://github.com/robinmoglia/my-first-repo)** (`readme.txt`, `install.sh`, 3 commits, `feature-script` merged into `main`).

## Commands used

| Part | Task | Command |
|---|---|---|
| 1 | Check the Git version | `git --version` |
| 1 | Check name and email | `git config --global --list` |
| 2 | Create the repository | `mkdir my-first-repo && cd my-first-repo && git init` |
| 2 | Create a file | `echo "My first Git repository" > readme.txt` |
| 3 | Check the status | `git status` |
| 3 | Stage one file | `git add readme.txt` |
| 3 | First commit | `git commit -m "Add readme file"` |
| 3 | Show the history | `git log` |
| 4 | Append a line | `echo "Second line" >> readme.txt` |
| 4 | Commit the change | `git add readme.txt && git commit -m "Add second line to readme"` |
| 5 | Show unstaged changes | `git diff` |
| 5 | Compact history | `git log --oneline` |
| 6 | List branches | `git branch` |
| 6 | Create a branch | `git branch feature-script` |
| 6 | Switch branch | `git switch feature-script` (or `git checkout feature-script`) |
| 6 | Create and switch in one command | `git switch -c dev` (or `git checkout -b dev`) |
| 7 | Make the script executable | `chmod +x install.sh` |
| 7 | Commit the script | `git add install.sh && git commit -m "Add install script"` |
| 8 | Merge into main | `git switch main && git merge feature-script` |
| 8 | Delete the merged branch | `git branch -d feature-script` |
| 9 | Link to GitHub and push | `git remote add origin https://github.com/robinmoglia/my-first-repo.git` then `git push -u origin main` |
| 10 | Get the repository back | `rm -rf my-first-repo && git clone https://github.com/robinmoglia/my-first-repo.git` |

## What I learned

- **Untracked, modified, staged**: a new file is *untracked* (red); a tracked file changed since the last commit is *modified* (red); after `git add` it is *staged* (green) and ready to be committed.
- **Staging vs committing**: `git add` prepares what will be saved; `git commit` records a snapshot of what was staged.
- **`git diff`** shows the lines added (`+`) or removed (`-`) since the last `git add`.
- **`git log` vs `git log --oneline`**: full hash, author and date, or one line per commit with the short hash.
- **The `*` in `git branch`** marks the branch you are currently on, and `HEAD` points to it.
- **Branches** are separate lines of development: work on a feature without breaking `main`, then merge it.
- **`install.sh` was not on `main` before the merge** because it was only committed on `feature-script`.
- **Fast-forward merge**: `main` had no new commit since the branch was created, so Git simply moved `main` forward; no merge commit was needed.
- **`#!/bin/bash`** (the shebang) tells the system which program runs the script, so it can be launched with `./install.sh`.
- **Git vs GitHub**: Git is the version control tool installed locally; GitHub is a website hosting Git repositories online.
- **`git init` vs `git clone`**: `init` turns an existing folder into a new, empty repository; `clone` downloads an existing remote repository with its whole history and links it to the remote.
- **"fatal: not a git repository"** means the current folder is not tracked by Git (no `git init`, or not inside the repository folder).
