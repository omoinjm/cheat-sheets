---
title: ArchLinux on WSL2 Setup Guide
description: A comprehensive guide for installing and configuring ArchLinux on WSL2, covering both Docker-based and basic installation methods, user setup, and essential tool installation.
type: content
path: systems/linux/setup.md
tags: [systems, linux, archlinux, wsl2, installation, setup]
---
# ArchLinux on WSL2 Setup Guide

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Linux operating system documentation, specifically detailing the setup and configuration of ArchLinux within the Windows Subsystem for Linux 2 (WSL2) environment.

## Contents Overview

This file provides comprehensive instructions for installing ArchLinux on WSL2 using both a Docker-based method and a basic installation approach. It covers user setup, `pacman` key management, installation of essential tools like `sudo` and `vim`, configuring `sudoers`, setting default users for WSL distros, and installing package managers like `yay` and environment tools like `direnv`. It also briefly mentions Protocol Buffers and gRPC in Go and references a WSL2 Docker start script.

## Role in System

This guide is crucial for developers and users who wish to leverage the power and flexibility of ArchLinux within a Windows development environment via WSL2. It streamlines the setup process and provides solutions for common configuration challenges.

## Installation Methods and Configuration

### Method 1: Install using Docker

This method involves pulling the ArchLinux Docker image, creating and starting a container, and then exporting it as a WSL2 distribution.

**Key Steps:**
1.  Pull `archlinux` Docker image.
2.  Create and start a Docker container.
3.  Configure `pacman-key`, add a new user to the `wheel` group, set password, update system, install `sudo` and `vim`.
4.  Edit `/etc/sudoers` to enable `wheel` group for `sudo`.
5.  Export the Docker container to a `.tar` file.
6.  Configure Windows Terminal to use the exported WSL2 ArchLinux instance with the newly created user.

### Method 2: Basic Installation

This alternative method uses pre-built ArchWSL releases and provides steps for further configuration.

**Key Steps:**
1.  Basic installation using `yuk7/ArchWSL` or similar resources.
2.  **Package Manager (`yay`):** Installation and usage of `yay`, an AUR helper.
    -   Update `pacman` and `pacman-key` for proper package management.
3.  **Set Default User for WSL Distro:** Configure `/etc/wsl.conf` to set a default user and manage user accounts.

### Additional Tools and Integrations

-   **Direnv Installation:** Instructions for setting up `direnv` for environment variable management.
-   **Protocol Buffers and gRPC in Go:** A reference for working with these technologies.
-   **WSL2 Docker Start Script:** A reference to a script for starting Docker within WSL2.

## References

-   [ArchWSL by yuk7](https://github.com/yuk7/ArchWSL)
-   [ArchLinuxWSL2 Gist](https://gist.github.com/ld100/3376435a4bb62ca0906b0cff9de4f94b#file-archlinuxwsl2-md)
-   [yay AUR Helper](https://github.com/Jguer/yay)
-   [Install yay on Arch Linux and Manjaro](https://www.tecmint.com/install-yay-aur-helper-in-arch-linux-and-manjaro/)
-   [Set default user for manually installed WSL distro](https://superuser.com/questions/1566022/how-to-set-default-user-for-manually-installed-wsl-distro)
-   [Set default user WSL Windows 10](https://winaero.com/set-default-user-wsl-windows-10/)
-   [Direnv Installation](https://direnv.net/docs/installation.html)
-   [Protocol Buffers and gRPC in Go](https://dev.to/karankumarshreds/protocol-buffers-and-grpc-in-go-3eil)
-   [wsl2-docker-start](https://github.com/imjonos/wsl2-docker-start)