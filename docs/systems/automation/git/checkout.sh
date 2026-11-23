# Git Checkout Automation Script (`checkout.sh`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the Git automation tools within the Linux operating system documentation, designed to streamline common Git repository management tasks.

## Contents Overview

The `checkout.sh` script is a powerful utility that automates the process of synchronizing all local Git repositories within a given directory structure. It fetches all remote branches, checks out each branch, pulls the latest changes, and manages a dedicated backup branch for each repository.

## Role in System

This script is invaluable for developers working with multiple Git repositories or needing to ensure all local branches are up-to-date. It simplifies repository maintenance, makes it easier to switch between branches, and provides a consistent way to manage backups.

## Usage

To use this script, simply execute it from the directory containing your Git repositories:

```bash
./checkout.sh
```

### Script Logic

1.  **Find Git Repositories**: It first identifies all subdirectories that are initialized Git repositories (by looking for a `.git` folder).
2.  **Fetch All**: For each identified repository, it runs `git fetch --all` to get the latest information from all remotes.
3.  **Checkout and Pull Branches**: It then iterates through all remote-tracking branches, checks out each one, and pulls the latest changes from its upstream.
4.  **Manage Backup Branch**:
    *   It attempts to create a unique backup branch (e.g., `backup/<dir>_<user.email>`).
    *   If the backup branch doesn't exist, it creates and checks it out.
    *   If it exists, it checks it out and pulls the latest changes.
    *   *Note: Pushing the new backup branch is commented out by default and can be enabled if desired.*

## Entry Points

-   Execution: `./checkout.sh`
-   Configuration: `git config --get user.email` is used to help name backup branches.

## Conventions

-   Assumes standard Git repository structure.
-   Requires `git` to be installed and configured in the system's PATH.
-   Uses `find`, `grep`, `sed`, `printf`, `git`, and `echo` commands.