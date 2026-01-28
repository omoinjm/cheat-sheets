# Setting up MySQL in a Docker Container

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on deploying and managing MySQL within Docker containers.

## Contents Overview

This file provides instructions and commands for setting up a MySQL database server within a Docker container. It covers pulling the official MySQL Docker image, running the container with necessary configurations (port mapping, environment variables), explanations of Docker command-line tags, and details for connecting to the running MySQL instance.

## Role in System

This guide is essential for developers and database administrators who need a quick, isolated, and consistent MySQL environment for development, testing, or microservice architectures. Dockerizing MySQL simplifies database setup and ensures portability across different environments.

## Key Concepts and Commands

### Setting up MySQL on Docker

1.  **Pull the MySQL Docker Image**:
    ```bash
    docker pull mysql
    ```

2.  **Run the MySQL Container**:
    Use the `docker run` command to start a new MySQL container. This example runs it in detached mode, maps port 3306, and sets the root password.

    ```bash
    docker run --name grooove-mysql \
    -p 3306:3306 \
    -e "MYSQL_ROOT_PASSWORD=<PASSWORD>" \
    -d mysql:latest
    ```
    *(For PowerShell, use backticks `` ` `` for line continuation instead of backslashes `\`)*

### Explanations of Docker Tags

-   `-d`: Runs the container in detached mode (in the background).
-   `-p <host_port>:<container_port>`: Maps the specified host port to the container's port. Here, host port `3306` is mapped to container port `3306`.
-   `-e <VAR>=<VALUE>`: Sets environment variables inside the container.
    -   `MYSQL_ROOT_PASSWORD=<PASSWORD>`: Sets the password for the `root` user in MySQL.
-   `--name <container_name>`: Assigns a custom name to the container for easier management.
-   `mysql:latest`: Specifies the Docker image name (`mysql`) and tag (`latest`) to use.

### Connect to the MySQL Instance

-   **Connection type**: MySQL
-   **Server**: `localhost` (or the IP address of your Docker host)
-   **Authentication type**: SQL Login
-   **User name**: `root`
-   **Password**: The `<PASSWORD>` you set with the `MYSQL_ROOT_PASSWORD` environment variable.
