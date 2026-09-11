---
title: Secure Linux Server Hardening
description: A 5-step guide to securing a Linux server, including automatic updates, limited user accounts, SSH key authentication, SSH hardening, and firewall setup.
type: content
path: workspace/networking/secure-shell.md
tags: [workspace, networking, linux, security, ssh, hardening, ufw]
---
# Secure Linux Server Hardening

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Linux operating system documentation, focusing on best practices for securing Linux servers.

## Contents Overview

This file outlines a 5-step process to secure a Linux server: enabling automatic updates, creating limited user accounts, using SSH keys for authentication (disabling passwords), hardening SSH configurations, and setting up a firewall. It includes practical commands and references to external resources.

## Role in System

This guide is essential for establishing a robust security posture for any Linux server, minimizing vulnerabilities and protecting against unauthorized access. It emphasizes a defense-in-depth approach, combining different security measures.

## 5 Steps to a Secure Linux Server

### 1. Enable Automatic Updates

Ensure your server is always running with the latest security patches.

**Manual Updates:**
```bash
apt update
apt dist-upgrade
```

**Automatic Updates:**
```bash
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

### 2. Create a Limited User Account

Operate with a non-root user account with `sudo` privileges for daily tasks.

**Commands:**
```bash
adduser <user>
usermod -aG sudo <user>
```

### 3. Get Rid of Password-Based Logins (Use SSH Keys)

Strengthen authentication by using SSH key pairs instead of passwords.

**Commands:**
-   `mkdir ~/.ssh && chmod 700 ~/.ssh`: Create `.ssh` directory.
-   `ssh-keygen -b 4096`: Generate SSH key pair on your local machine.
-   `scp` or `ssh-copy-id` to transfer your public key to the server's `~/.ssh/authorized_keys`.

### 4. Lockdown Logins (Harden SSH)

Further secure SSH by disabling root login and password authentication, and changing the default SSH port.

**Configuration (`/etc/ssh/sshd_config`):**
```
Port <pick different number>
AddressFamily inet
PermitRootLogin no
PasswordAuthentication no
```
**Restart SSH service:** `sudo systemctl restart sshd`

### 5. FIREWALL IT UP (UFW)

Configure a firewall (UFW) to control incoming and outgoing traffic.

**Commands:**
-   `sudo apt install ufw`: Install UFW.
-   `sudo ufw status`: Check firewall status.
-   `sudo ufw allow {port number}`: Allow specific ports.
-   `sudo ufw enable`: Enable the firewall.
-   `sudo ufw reload`: Reload firewall rules.
-   Drop pings: Edit `/etc/ufw/before.rules` and add `-A ufw-before-input -p icmp --icmp-type echo-request -j DROP`.

## References

-   Detailed guide from [networkchuck](https://learn.networkchuck.com/courses/take/ad-free-youtube-videos/lessons/22626695-protect-your-linux-server-from-hackers-5-steps)
