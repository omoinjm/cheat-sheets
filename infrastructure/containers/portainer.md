---
title: Docker - Portainer Community Edition Setup
description: A guide for setting up Portainer CE using Docker Compose, including service definitions, networking, and volume configuration.
type: content
path: infrastructure/containers/portainer.md
tags: [infrastructure, containers, docker, portainer, management]
---
# Docker - Portainer Community Edition Setup

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the [Docker](./linux-docker.md) containerization knowledge base, specifically focusing on deploying Portainer using Docker Compose.

## Contents Overview

This file provides a [Docker](./linux-docker.md) Compose configuration example for deploying Portainer Community Edition (CE), a powerful web-based UI for managing [Docker](./linux-docker.md) environments. It outlines the service definition, port mappings, network configuration, volume mounts, and restart policy.

## Role in System

Portainer simplifies the management of [Docker](./linux-docker.md) containers, images, volumes, and networks through an intuitive graphical interface. This document helps users quickly deploy Portainer to gain better visibility and control over their [Docker](./linux-docker.md) deployments, especially when running multiple containers or managing complex setups.

## Docker Compose Configuration for Portainer CE

### `docker-compose.yml` Example

The following `docker-compose.yml` file defines the Portainer CE service:

```yaml
version: '3.3'
services:
  portainer-ce:
    ports:
      - '9000:9000' # Port for the Portainer web UI
      - '8000:8000' # Edge agent port (if used)
    container_name: portainer
    networks:
      - nginxproxymanager_default # Connects to an external network, e.g., created by Nginx Proxy Manager
    restart: always # Always restart the container unless stopped manually
    volumes:
      - '/var/run/docker.sock:/var/run/docker.sock' # Mount the Docker socket for Portainer to manage Docker
      - '/home/ubuntu/docker/portainer:/data'      # Persistent storage for Portainer's data
    image: 'portainer/portainer-ce:latest' # Official Portainer Community Edition image

networks:
  nginxproxymanager_default:
    external: true # Specifies that this network is external and should already exist
```

### Running the Stack

To deploy Portainer CE using this Docker Compose file, navigate to the directory containing the `docker-compose.yml` and execute:

```bash
docker-compose up -d
```

This command will pull the `portainer/portainer-ce:latest` image, create the Portainer container, and start it in detached mode (in the background). After deployment, you can usually access the Portainer UI via `http://<your-server-ip>:9000`.

### Key Configuration Details

-   **`image: 'portainer/portainer-ce:latest'`**: Specifies the Docker image for Portainer Community Edition.
-   **`container_name: portainer`**: Assigns a static name to the container.
-   **`ports`**:
    -   `9000:9000`: Maps host port 9000 to container port 9000 for the main web UI.
    -   `8000:8000`: Maps host port 8000 to container port 8000, typically used for the Edge agent communications.
-   **`networks`**: Connects the Portainer container to an external network (e.g., `nginxproxymanager_default`), allowing it to communicate with other services on that network.
-   **`restart: always`**: Ensures Portainer automatically restarts if it crashes or the Docker daemon restarts.
-   **`volumes`**:
    -   `/var/run/docker.sock:/var/run/docker.sock`: This crucial mount allows Portainer to communicate with the Docker daemon and manage containers on the host.
    -   `/home/ubuntu/docker/portainer:/data`: Mounts a host directory for persistent storage of Portainer's configuration and data.
