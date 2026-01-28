# Docker - OSINT with PhoneInfoga

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on utilizing Docker for Open-Source Intelligence (OSINT) tools.

## Contents Overview

This file provides a quick guide on how to use `PhoneInfoga`, a popular OSINT tool for gathering information about phone numbers, within a Docker container. It includes commands for pulling the Docker image, checking its version, performing scans directly from the terminal, and launching its web-based user interface.

## Role in System

Docker enables security researchers and analysts to quickly deploy and run specialized OSINT tools like PhoneInfoga in an isolated and consistent environment, without worrying about dependency conflicts or system-specific setups. This document facilitates the rapid deployment of such tools for intelligence gathering.

## PhoneInfoga - OSINT Phone Number Tool

-   **Official Getting Started Guide**: [PhoneInfoga Getting Started Guide](https://sundowndev.github.io/phoneinfoga/getting-started/install/)

### Key Docker Commands for PhoneInfoga

1.  **Download the Docker Image**:
    ```bash
    docker pull sundowndev/phoneinfoga:latest
    ```

2.  **Check the Version**:
    ```bash
    docker run --rm -it sundowndev/phoneinfoga version
    ```
    -   `--rm`: Automatically remove the container when it exits.
    -   `-it`: Run in interactive mode with a pseudo-TTY, allowing interaction.

3.  **Run a Scan in the Terminal**:
    Replace `<number>` with the target phone number.
    ```bash
    docker run --rm -it sundowndev/phoneinfoga scan -n <number>
    ```

4.  **Access the Web UI**:
    This command starts the PhoneInfoga web interface, accessible via your browser at `http://localhost:8080`.
    ```bash
    docker run --rm -it -p 8080:8080 sundowndev/phoneinfoga serve -p 8080
    ```
    -   `-p 8080:8080`: Maps host port 8080 to container port 8080.
