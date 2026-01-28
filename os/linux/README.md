# Linux Operating System

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README](../../README.md)

## Contents Overview

This directory contains documentation, configurations, and scripts tailored for Linux-based operating systems. It covers a range of topics from basic setup to advanced configurations, automation, and security.

### Subdirectories

-   [automation](./automation/README.md): Scripts and notes for automating various tasks on Linux.
-   [images](./images/README.md): Images and diagrams related to Linux configurations and concepts.

### Files

-   [cron-jobs.md](./cron-jobs.md): Documentation on scheduling tasks using cron jobs.
-   [docker.md](./docker.md): Notes and commands related to Docker on Linux.
-   [mssql.md](./mssql.md): Information about Microsoft SQL Server on Linux.
-   [nginx.md](./nginx.md): Configuration and usage of Nginx web server.
-   [password-store.md](./password-store.md): Documentation for managing passwords securely.
-   [postgres.md](./postgres.md): Notes on PostgreSQL database setup and management.
-   [secure-shell.md](./secure-shell.md): Guides for securing SSH access.
-   [setup.md](./setup.md): General Linux setup procedures.
-   `README.md`: This file, providing an overview of Linux-related documentation.

## Role in System

This section serves as a comprehensive knowledge base for Linux users and administrators. It provides quick access to configurations, troubleshooting steps, and best practices for common Linux tools and services.

## Useful Information from Original README

### ZSH / BASH dotfiles

References for dotfile configurations:
-   [Takuya](https://github.com/craftzdog/dotfiles-public)
-   [ChristianLempa](https://github.com/ChristianLempa/dotfiles)
-   [subho007](https://github.com/subho007/.dotfile)

### Change Hostname

To change the hostname on Ubuntu:
```bash
hostnamectl set-hostname new-hostname

# Set pretty name
hostnamectl set-hostname "new-hostname" --pretty
```
Reference: [Change Hostname](https://phoenixnap.com/kb/ubuntu-20-04-change-hostname)

### Install .NET SDK or Runtime on Ubuntu

Refer to the official Microsoft documentation: [Install .NET on Ubuntu](https://docs.microsoft.com/en-us/dotnet/core/install/linux-ubuntu?source=recommendations#2004)

### Set up an SSH key

Refer to Atlassian documentation: [Set up an SSH key](https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/)

### Permanently authenticating with Git repositories

Refer to Atlassian documentation: [Permanently authenticating with Git repositories](https://confluence.atlassian.com/bitbucketserver/permanently-authenticating-with-git-repositories-776639846.html)

### How to make files accessible only by root?

```bash
sudo chown root:root /path/to/application
sudo chmod 700 /path/to/application
```
Reference: [How to make files accessible only by root?](https://askubuntu.com/questions/193055/how-to-make-files-accessible-only-by-root)

### How to Install OpenVPN in Ubuntu 20.04?

Refer to Tecmint guide: [Install OpenVPN in Ubuntu](https://www.tecmint.com/install-openvpn-in-ubuntu/)

### How to Create and Use Symbolic Links

```bash
ln -s /path/to/original /path/to/link
```
Reference: [How to Create and Use Symbolic Links](https://www.howtogeek.com/287014/how-to-create-and-use-symbolic-links-aka-symlinks-on-linux/)

### LSD (LSDeluxe)

A modern `ls` command replacement with enhanced features.
-   [Link](https://github.com/Peltoche/lsd)
-   [Video](https://www.youtube.com/watch?v=8q1NDEKkSf4)

### Fuzzy Finder (fzf)

A general-purpose command-line fuzzy finder.
-   [GitHub](https://github.com/junegunn/fzf)
-   [GeeksforGeeks](https://www.geeksforgeeks.org/fzf-file-search-from-linux-terminal/)
-   [Bytexd](https://bytexd.com/how-to-use-fzf-command-line-fuzzy-finder/)