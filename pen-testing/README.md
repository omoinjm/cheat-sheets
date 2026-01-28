---
type: directory
path: pen-testing
parent: .
tags: [repo, documentation, security, pen-testing]
---
# Penetration Testing Knowledge Base

## 🔗 Navigation
- [[../README|⬆ Parent]]
- [[../README|🏠 Root]]
- [[./|📂 Current Directory]]

## 📌 Overview
This directory serves as a knowledge base for penetration testing, covering various tools, methodologies, and notes from practical exercises (e.g., Hack The Box) and reverse engineering. It is dedicated to accumulating and organizing information vital for security research, vulnerability assessment, and ethical hacking.

## 📁 Contents
- [[htb/README|htb]]: Notes and resources from Hack The Box (HTB) challenges.
- [[reserve-engineering/README|reserve-engineering]]: Documentation and findings related to reverse engineering efforts.
- [[README.md]]: This file, providing an overview of penetration testing documentation.

## 🧠 Responsibilities
This directory is responsible for centralizing information on cybersecurity, including techniques, tools, and learning experiences from penetration testing and reverse engineering. It acts as a quick reference for security professionals.

## 🔄 Relationships
This directory is a direct child of the root. Its content is highly related to [[../os/README|operating system]] specific configurations for security, and it may reference tools and concepts found in the [[../languages/README|languages]] section for exploit development or analysis.

## 🛠️ Key Tools and Techniques

### Hakrawler
- **Description**: A fast Golang web crawler designed to gather URLs and JavaScript file locations, built upon the Gocolly library.
- **Link**: [Hakrawler GitHub Repository](https://github.com/hakluke/hakrawler)

### Nmap Scan
- **Command**: Perform a SYN scan and version detection.
    ```bash
    sudo nmap -sS -sV <ip address>
    ```

### Connecting to Different Protocols/Services
- **Telnet**:
    - Port: `22/tcp`
    - Command: `telnet <ip address>`

- **FTP**:
    - Port: `21/tcp`
    - Command: `ftp <ip address>`

- **SMB**:
    - Port: `445/tcp`
    - Command: `smbclient //ip address/Sharename`
