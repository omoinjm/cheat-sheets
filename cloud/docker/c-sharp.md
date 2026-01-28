# Dockerizing ASP.NET Web API (C#)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Docker containerization knowledge base, specifically focusing on integrating Docker with C# and ASP.NET applications.

## Contents Overview

This file provides a comprehensive guide to containerizing an ASP.NET Web API application using Docker. It includes a multi-stage Dockerfile for building and serving the application, commands for building and running Docker images, and detailed explanations of various `docker run` options and environment variables.

## Role in System

This guide is essential for C# developers looking to leverage Docker for consistent development environments, efficient deployment, and scalable hosting of their ASP.NET Web APIs. It streamlines the process of moving .NET applications into containerized ecosystems.

## Key Concepts and Commands

### Dockerfile Example

A multi-stage Dockerfile for building and publishing an ASP.NET 6.0 Web API:

```dockerfile
# See https://aka.ms/customizecontainer to learn how to customize your debug container
# and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 5000

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["./Grooove_Web_API.csproj", "./"]
RUN dotnet restore "./Grooove_Web_API.csproj"
COPY . .
WORKDIR /src
RUN dotnet build "./Grooove_Web_API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Grooove_Web_API.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Grooove_Web_API.dll"]
```

### Build the Docker Image

```bash
# Build the image from the Dockerfile
docker build --rm -t omoi/grooovewebapi:latest .

# Show/view images
docker image ls
```

### Run the Docker Image

Commands to run the container, including port mapping and environment variable setup.

-   **Example with specific environment variables**:
    ```bash
docker run -d --name insurance_poc_api \
    -p 5000:5000 -p 5242:5242 \
    -e ASPNETCORE_HTTP_PORT=https://+:5000 \
    -e ASPNETCORE_URLS=http://+:5242 \
    -e ASPNETCORE_ENVIRONMENT=Development \
    -e POSTGRES_CONNECTION_STRING="host=ep-restless-art-a4tqr4a4-pooler.us-east-1.aws.neon.tech; Port=5432; Username=default; Password=Z8VkpMit4NPr; Database=verceldb; SslMode=Require;" \
    omoi/insurance-poc:latest
    ```

-   **Basic run command (detached)**:
    ```bash
docker run -d --name grooove_api \
-p 5000:5000 -p 5001:5001 \
-e ASPNETCORE_HTTP_PORT=https://+:5001 \
-e ASPNETCORE_URLS=http://+:5000 \
omoi/grooovewebapi
    ```

-   **Run and remove on exit**:
    ```bash
docker run --rm -it --name grooove_api \
-p 5000:5000 -p 5001:5001 \
--env-file .env \
-e ASPNETCORE_HTTP_PORT=https://+:5001 \
-e ASPNETCORE_URLS=http://+:5000 \
omoi/grooovewebapi
    ```

### Explanations of `docker run` Tags

-   `--env-file`: Adds a file containing environment variables.
-   `-it`: Runs the container interactively, connected to the terminal, showing output.
-   `-p <host_port>:<container_port>`: Maps host ports to container ports (e.g., `-p 5000:5000`).
-   `-e <VAR>=<VALUE>`: Sets an environment variable inside the container.
    -   `ASPNETCORE_HTTP_PORT=https://+:5001`: Sets ASP.NET Core to listen on HTTPS port 5001.
    -   `ASPNETCORE_URLS=http://+:5000`: Sets ASP.NET Core to listen on HTTP port 5000.