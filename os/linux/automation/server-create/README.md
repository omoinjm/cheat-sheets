---
type: directory
path: os/linux/automation/server-create
parent: os/linux/automation
tags: [repo, documentation, os, linux, automation, server, aws, lamp]
---
# Server Creation Automation

## 🔗 Navigation
- [[../README|⬆ Parent]]
- [[../../../../README|🏠 Root]]
- [[./|📂 Current Directory]]

## 📌 Overview
This directory contains shell scripts designed to automate the creation of virtual machines on cloud platforms and the installation of common server stacks on Linux. These scripts aim for rapid and consistent deployment of new server instances.

## 📁 Contents
- [[create_aws_ubuntu_vm.sh]]: A script for automating the creation of an Ubuntu Virtual Machine on Amazon Web Services (AWS).
- [[setup_lamp_server.sh]]: A script for automating the setup of a LAMP (Linux, Apache, MySQL, PHP) server stack.
- [[README.md]]: This file, providing an overview of server creation automation scripts.

## 🧠 Responsibilities
This directory is responsible for providing automated solutions for provisioning and configuring server environments on Linux. It aims to reduce manual configuration errors and accelerate development and deployment workflows.

## 🔄 Relationships
This directory is a child of the [[../README|automation]] directory. The scripts here interact with [[../../../../cloud/aws/README|AWS]] infrastructure and are related to general [[../../../../cloud/README|cloud]] concepts. They can be used to set up environments for applications documented in the [[../../../../languages/README|languages]] section.