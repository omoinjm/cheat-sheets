---
title: Run SQL Server in a Docker Container
description: A comprehensive guide for running Microsoft SQL Server in a Docker container, including standalone and Docker Compose setups.
type: content
path: development/databases/mssql-docker.md
tags: [development, databases, mssql, docker, containerization, sql-server]
---
# Run SQL Server in a Docker Container

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on deploying and managing Microsoft SQL Server within Docker containers.

## Contents Overview

This file provides comprehensive instructions for running Microsoft SQL Server in a Docker container. It covers single-container deployments using `docker run` commands (with and without named volumes), explanations of key Docker flags, steps to connect to the SQL instance, and a full Docker Compose setup for a more robust, multi-service deployment with a custom Dockerfile.

## Role in System

This guide is crucial for developers and database administrators who need a portable, isolated, and easily reproducible SQL Server environment for development, testing, or even lightweight production scenarios. Dockerizing SQL Server simplifies setup and integration into CI/CD pipelines.

## Key Concepts and Commands

### Running a Standalone SQL Server Container

#### Commands

-   **Create a Docker Volume (recommended for persistence)**:
    ```bash
docker volume create docker-mssql-data
```
-   **Run SQL Server container with a named volume**:
    ```bash
docker run -d \
-p 1435:1433 \
-e "ACCEPT_EULA=Y" \
-e "SA_PASSWORD=<PASSWORD>" \
--name docker-sqlserver-2019 \
--mount source=docker-mssql-data,target=/var/opt/mssql \
mcr.microsoft.com/mssql/server:2019-latest
```
-   **Run SQL Server container with host-mounted volumes (keeps data on local machine)**:
    ```bash
docker run -d \
-p 1433:1433 \
-e 'ACCEPT_EULA=Y' \
-e 'MSSQL_SA_PASSWORD=<PASSWORD>' \
-v '/mnt/d/omoi/data/docker/volumes/data':/var/opt/mssql/data \
-v '/mnt/d/omoi/data/docker/volumes/log':/var/opt/mssql/log \
-v '/mnt/d/omoi/data/docker/volumes/secrets':/var/opt/mssql/secrets \
--name sqlserver-2019 \
mcr.microsoft.com/mssql/server:2019-latest
```

#### Key Docker Tags Explained

-   `-d`: Runs the container in detached (background) mode.
-   `-p <host_port>:<container_port>`: Maps a port from the container to the host machine.
-   `-e <VAR>=<VALUE>`: Sets environment variables inside the container (e.g., `ACCEPT_EULA`, `SA_PASSWORD`).
-   `-v <source>:<target>` / `--mount`: Mounts a volume for data persistence.
-   `--name`: Assigns a human-readable name to the container.
-   `mcr.microsoft.com/mssql/server:2019-latest`: The Docker image name and tag.

#### Connecting to the SQL Instance

-   **Connection type**: Microsoft SQL Server
-   **Server**: `localhost` (or the host's IP)
-   **Authentication type**: SQL Login
-   **User name**: `sa`
-   **Password**: The password specified during container creation.

### Docker Compose Setup

This section outlines how to define a multi-service application with SQL Server using `docker-compose.yml` and a custom `Dockerfile`.

#### `docker-compose.yml` Example

```yaml
version: '3.8'
services:
  identity-database:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      - "1433:1433"
    env_file:
      - MSSQL_SA_PASSWORD=<sql-server-admin-password>
      - ACCEPT_EULA=Y
      - MSSQL_DATA_DIR=/var/opt/sqlserver/data
      - MSSQL_LOG_DIR=/var/opt/sqlserver/log
      - MSSQL_BACKUP_DIR=/var/opt/sqlserver/backup
    volumes:
      - sqlsystem:/var/opt/mssql/
      - sqldata:${MSSQL_DATA_DIR}
      - sqllog:${MSSQL_LOG_DIR}
      - sqlbackup:${MSSQL_BACKUP_DIR}
volumes:
  sqlsystem:
  sqldata:
  sqllog:
  sqlbackup:
```

#### Custom `Dockerfile` Example

A custom Dockerfile to build a SQL Server image based on Ubuntu, installing SQL Server and setting up directory permissions:

```dockerfile
FROM ubuntu:20.10
RUN useradd -u 10001 mssql
# ... (installation and directory setup commands) ...
USER mssql
CMD /opt/mssql/bin/sqlservr
```

#### Running with Docker Compose

```bash
docker-compose up -d
```
