---
title: Cron Jobs
description: A quick guide to managing cron jobs in Linux, including editing, listing, and troubleshooting.
type: content
path: systems/linux/cron-jobs.md
tags: [systems, linux, cron, automation]
---
# Cron Jobs

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Linux operating system documentation, focusing on task automation.

## Contents Overview

This file provides a quick guide on how to manage cron jobs in Linux. It includes commands for editing the crontab, adding new jobs, verifying their setup, and troubleshooting their execution.

## Role in System

Cron jobs are essential for automating repetitive tasks on a Linux system, such as backups, system maintenance, or custom script execution. This document serves as a reference for setting up and managing these automated tasks.

## Key Commands

-   `crontab -e`: Open the crontab file for editing.
-   `crontab -l`: List currently scheduled cron jobs.
-   `systemctl status cron`: Check the status of the cron daemon.