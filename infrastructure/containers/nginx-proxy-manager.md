---
title: Docker - Nginx Proxy Manager Setup
description: A guide for setting up Nginx Proxy Manager using Docker Compose, including port mapping and volume configuration for SSL management.
type: content
path: infrastructure/containers/nginx-proxy-manager.md
tags: [infrastructure, containers, docker, nginx, proxy-manager, ssl]
---
# Docker - Nginx Proxy Manager Setup

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on deploying Nginx Proxy Manager using Docker Compose.

## Contents Overview

This file provides a Docker Compose configuration example for setting up Nginx Proxy Manager, a popular tool for easily managing Nginx proxy hosts, SSL certificates, and custom streams. It outlines the service definition, port mappings, and volume configurations.

## Role in System

Nginx Proxy Manager simplifies the process of securely exposing web services running in Docker containers or on a local network. This document helps users quickly deploy this essential tool to manage reverse proxies, handle SSL termination with Let's Encrypt, and centralize access to multiple web applications.

## Docker Compose Configuration for Nginx Proxy Manager

### `docker-compose.yml` Example

The following `docker-compose.yml` file defines the Nginx Proxy Manager service:

```yaml
version: '3.8'
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'    # HTTP port
      - '81:81'    # Admin UI port
      - '443:443'  # HTTPS port
      # - '9443:9443' # Example for Portainer, if used
    volumes:
      - ./data:/data              # Persistent data for Nginx Proxy Manager
      - ./letsencrypt:/etc/letsencrypt # Persistent storage for Let's Encrypt certificates
```

### Running the Stack

To deploy Nginx Proxy Manager using this Docker Compose file, navigate to the directory containing the `docker-compose.yml` and execute:

```bash
docker-compose up -d
```

This command will pull the `jc21/nginx-proxy-manager:latest` image, create the necessary containers, and start them in detached mode (in the background).

### Key Configuration Details

-   **`image: 'jc21/nginx-proxy-manager:latest'`**: Specifies the Docker image for Nginx Proxy Manager.
-   **`restart: unless-stopped`**: Ensures the container restarts automatically unless explicitly stopped.
-   **`ports`**:
    -   `80:80`: Maps host port 80 to container port 80 for HTTP traffic.
    -   `81:81`: Maps host port 81 to container port 81, which is typically used for the Nginx Proxy Manager admin interface.
    -   `443:443`: Maps host port 443 to container port 443 for HTTPS traffic.
-   **`volumes`**:
    -   `./data:/data`: Mounts a local `data` directory to `/data` inside the container for persistent application data.
    -   `./letsencrypt:/etc/letsencrypt`: Mounts a local `letsencrypt` directory to `/etc/letsencrypt` inside the container for persistent storage of SSL certificates.
