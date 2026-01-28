# Git Configuration Automation Script (`git_config.sh`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the Git automation tools within the Linux operating system documentation, designed to standardize Git configurations across multiple repositories.

## Contents Overview

The `git_config.sh` script automates the process of setting the `user.name`, `user.email`, and `core.sshCommand` for all Git repositories found within the current directory and its subdirectories. It takes username, email, and an optional company name as arguments, validating them before applying the configurations.

## Role in System

This script is highly beneficial for developers who contribute to multiple projects with different Git identities or who need to quickly set up a new development environment. It ensures consistency in commit authorship and simplifies the management of SSH keys for different Git hosts, especially in environments where specific SSH keys are tied to particular accounts or organizations.

## Usage

To use this script, execute it with your desired username, email, and optionally a company name:

```bash
./git_config.sh "Your Name" "your.email@example.com" [company_name]
```

-   `<username>`: The name to be used in Git commits.
-   `<email>`: The email address to be used in Git commits.
-   `<company_name>` (optional): Used to construct the path to the SSH key (e.g., `~/.ssh/work/<company_name>/id_rsa_<company_name>`). If not provided, it attempts to extract the company name from the email address.

### Script Logic

1.  **Argument Parsing and Validation**: The script parses the provided arguments and validates their format (username, email, company name length and characters).
2.  **Find Git Repositories**: It identifies all subdirectories that are initialized Git repositories.
3.  **Configure Git**: For each identified repository, it navigates into the directory and sets:
    *   `user.name`: The provided username.
    *   `user.email`: The provided email.
    *   `core.sshCommand`: Configures the SSH command to use a specific SSH key based on the provided company name, allowing for per-repository SSH key usage.

## Entry Points

-   Execution: `./git_config.sh <username> <email> [company]`
-   Configuration: Modifies `.git/config` within each repository. Expects SSH keys to be organized under `~/.ssh/work/<company>/id_rsa_<company>`.

## Conventions

-   Assumes standard Git repository structure.
-   Requires `git` and `ssh` to be installed and configured in the system's PATH.
-   Uses `find`, `echo`, `grep`, `sed`, `git`, and `printf` commands.
