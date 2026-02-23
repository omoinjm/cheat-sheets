# Terminal Password Manager (pass)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Linux operating system documentation, providing guidance on secure password management from the terminal.

## Contents Overview

This file serves as a comprehensive guide to `pass`, the standard Unix password manager. It covers key generation, password store initialization, creating and managing passwords, organizing entries, integrating with Git for backup, transferring the store to other machines, and integrating `pass` into daily workflows, including securing CLI commands with environment variables.

## Role in System

The `pass` utility is crucial for securely managing sensitive credentials directly from the command line, offering strong encryption and integration with version control systems for backup and synchronization. This document facilitates the adoption and effective use of this essential security tool.

## Key Topics and Commands

### GPG Key Management

-   `gpg --gen-key`: Generate a new GPG key pair.
-   `gpg -K`: List GPG keys.
-   `gpg --edit-key <key-id>`: Edit key properties, such as expiration date.
-   Exporting public and private keys for transfer to other machines.

### Password Store Initialization

-   `pass init <key-id>`: Initialize a new password store with your GPG key.
-   `pass init git`: Convert the password store into a Git repository for version control and backup.

### Password Management

-   `pass insert <name>`: Interactively insert a new password.
-   `pass generate <name>`: Generate a new strong password.
-   `pass show <name>`: Display a password.
-   `pass show -c <name>`: Copy a password to the clipboard.
-   `pass edit <name>`: Edit a password entry (can include metadata like email).
-   `pass rm <name>`: Remove a password entry.

### Organization and Search

-   `pass generate github/personal`: Create nested password entries.
-   `pass`: List all passwords.
-   `pass find <pattern>`: Search for passwords.
-   `pass grep <pattern>`: Search within password file contents (e.g., for email addresses).

### Git Integration and Synchronization

-   `pass git remote add origin <repo-url>`: Add a remote repository for backup.
-   `pass git push origin main`: Push changes to the remote.
-   `pass git clone <repo-url> .password-store`: Clone the store to another machine.
-   `pass git log`, `pass git revert HEAD`: Manage password history.

### Workflow Integration

-   Using `export` with `pass show` to set environment variables for sensitive tokens (e.g., `export GITHUB_TOKEN=$(pass show github/api/token)`).
-   Aliasing CLI commands to inject credentials from `pass` securely (e.g., for AWS CLI).