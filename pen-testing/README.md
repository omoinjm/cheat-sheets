# Penetration Testing Knowledge Base

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../README.md)

## Contents Overview

This directory serves as a knowledge base for penetration testing, covering various tools, methodologies, and notes from practical exercises (e.g., Hack The Box) and reverse engineering.

### Subdirectories

-   [htb](./htb/README.md): Notes and resources from Hack The Box (HTB) challenges.
-   [reserve-engineering](./reserve-engineering/README.md): Documentation and findings related to reverse engineering efforts.

## Role in System

This section is dedicated to accumulating and organizing information vital for security research, vulnerability assessment, and ethical hacking. It acts as a quick reference for techniques, tools, and learning experiences in the field of cybersecurity.

## Key Tools and Techniques

### Hakrawler

-   **Description**: A fast Golang web crawler designed to gather URLs and JavaScript file locations, built upon the Gocolly library.
-   **Link**: [Hakrawler GitHub Repository](https://github.com/hakluke/hakrawler)

### Nmap Scan

-   **Command**: Perform a SYN scan and version detection.
    ```bash
    sudo nmap -sS -sV <ip address>
    ```

### Connecting to Different Protocols/Services

-   **Telnet**:
    -   Port: `22/tcp`
    -   Command: `telnet <ip address>`

-   **FTP**:
    -   Port: `21/tcp`
    -   Command: `ftp <ip address>`

-   **SMB**:
    -   Port: `445/tcp`
    -   Command: `smbclient //ip address/Sharename`