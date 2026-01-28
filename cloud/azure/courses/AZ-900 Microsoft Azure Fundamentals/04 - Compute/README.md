# AZ-900 Module 04 - Compute Services

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../../../README.md)

## Parent Context

This directory contains the "Compute Services" module for the AZ-900 Microsoft Azure Fundamentals certification course.

## Contents Overview

This module explores Azure's various compute offerings, from virtual machines to serverless functions and container orchestration. It covers the core services used to run applications and workloads in the cloud, including Virtual Machines, Scale Sets, App Services, Container Instances, Azure Kubernetes Service, Azure Virtual Desktop, and Azure Functions.

### Subdirectories

-   [images](./images/README.md): Visual aids and diagrams related to Azure compute services.

### Files

-   [app-services.md](./app-services.md): Details about Azure App Services for hosting web apps, APIs, and mobile backends.
-   [azure-container-instances.md](./azure-container-instances.md): Information on running containers directly on Azure without managing servers.
-   [azure-kubernetes.md](./azure-kubernetes.md): Notes on Azure Kubernetes Service (AKS) for orchestrating containers.
-   [azure-virtual-desktop.md](./azure-virtual-desktop.md): Explains Azure Virtual Desktop for virtualized Windows experiences.
-   [functions.md](./functions.md): Covers Azure Functions, Azure's serverless compute offering.
-   [scale-sets.md](./scale-sets.md): Details about Azure Virtual Machine Scale Sets for automatic scaling of VMs.
-   [virtual-machines.md](./virtual-machines.md): Explores Azure Virtual Machines as IaaS compute.

## Role in System

This module is crucial for understanding how to deploy and manage application workloads in Azure. It provides insights into choosing the right compute service based on application requirements, scalability needs, and management preferences.

## Compute Summary

### [Virtual Machines](./virtual-machines.md)

-   Virtualized hardware you control.
-   Spin up and down as needed.
-   Take advantage of the Azure tools available. Priced per hour with many configurations available.

### [Scale Sets](./scale-sets.md)

-   Sets of identical VMs.
-   Scale sets automatically create and delete VMs for your application.
-   Provides high availability and protects against server failures.

### [App Services](./app-services.md)

-   Managed platform to host your applications.
-   Web app, containers, and API.
-   Supports a lot of programming languages.

### [Azure Container Instances](./azure-container-instances.md)

-   Hosts and runs your containers on Azure.
-   Containers have less overhead than virtual machines and can be deployed consistently.

### [Azure Kubernetes Service](./azure-kubernetes.md)

-   Open-source tool for orchestrating and managing many container images and applications.
-   Uses clusters and pods to scale and deploy applications.

### [Azure Virtual Desktop](./azure-virtual-desktop.md)

-   100% virtualized Windows 10.
-   Access with any device that has a browser and internet connection.
-   Reuse licenses to save some bananas.

### [Functions](./functions.md)

-   Serverless Azure offering.
-   A function does one compute action each time it is invoked.
