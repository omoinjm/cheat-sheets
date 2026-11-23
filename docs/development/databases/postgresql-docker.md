---
title: Run PostgreSQL in a Docker Container
description: A comprehensive guide for running PostgreSQL in a Docker container, including standalone and Docker Compose setups with pgAdmin.
type: content
path: development/databases/postgresql-docker.md
tags: [development, databases, postgresql, docker, containerization, pgadmin]
---
# Run PostgreSQL in a Docker Container

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on deploying and managing PostgreSQL within Docker containers.

## Contents Overview

This file provides instructions for running PostgreSQL in a Docker container, covering single-container deployments using `docker run` commands, a link to an external guide for backing up and restoring PostgreSQL databases, and a comprehensive Docker Compose setup that includes both PostgreSQL and pgAdmin (a web-based PostgreSQL administration tool).

## Role in System

This guide is crucial for developers and database administrators who need a quick, isolated, and consistent PostgreSQL environment for development, testing, or microservice architectures. Dockerizing PostgreSQL simplifies database setup and ensures portability across different environments.

## Key Concepts and Commands

### Running a Standalone PostgreSQL Container

#### Commands

1.  **Pull the PostgreSQL Docker Image**:
    ```bash
    docker pull postgres
    ```
2.  **Run the PostgreSQL Container**:
    Use the `docker run` command to start a new PostgreSQL container in detached mode, mapping port 5432, and setting the `POSTGRES_PASSWORD`.
    ```bash
    docker run --name grooove-postgresql \
    -p 5432:5432 \
    -e "POSTGRES_PASSWORD=<PASSWORD>" \
    -d postgres:latest
    ```
    *(For PowerShell, use backticks `` ` `` for line continuation instead of backslashes `\`)*

### Backup / Restore PostgreSQL Database

For a step-by-step guide on how to back up and restore PostgreSQL databases:

-   [Backup and Restore PostgreSQL Database](https://www.tecmint.com/backup-and-restore-postgresql-database/)

**Example `pg_dump` command:**
```bash
sudo pg_dump --dbname=NAME --username=USER > grooove_bak.sql
```

### Docker Compose Setup for PostgreSQL with pgAdmin

This section outlines how to define a multi-service application with PostgreSQL and pgAdmin using `docker-compose.yml`.

#### `docker-compose.yml` Example

```yaml
version: '3.8'
services:
  db:
    container_name: postgres_container
    image: postgres:latest
    restart: always
    ports:
      - "5432:5432"
    volumes:
            - db:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres

  pg-admin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    restart: always
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  db:
    driver: local
```

#### Running with Docker Compose

To deploy the PostgreSQL and pgAdmin stack using this Docker Compose file, execute:

```bash
docker-compose up -d
```
This command will start both the PostgreSQL database and the pgAdmin web interface in detached mode. pgAdmin will typically be accessible via `http://localhost:5050`.
