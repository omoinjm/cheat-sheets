# Azure Container Instances (ACI)

[⬆ Back to Parent](../04%20-%20Compute/README.md)
[🏠 Back to Root README (../../../../../../../README.md)

## Parent Context

This document is part of the "Compute Services" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file introduces Azure Container Instances (ACI), a service that enables running Docker containers directly on Azure without managing virtual machines or orchestrators. It highlights ACI's key features, typical workflow, and benefits, such as on-demand container execution and tool flexibility.

## Role in System

ACI is ideal for scenarios requiring single, isolated containers or simple containerized applications without the overhead of full container orchestration platforms. This document explains how ACI provides a fast and cost-effective way to run containers in Azure, simplifying deployment for many use cases.

## Key Concepts and Features

### Features

-   ![Features](./images/aci-features.png)

### Workflow

1.  **Application Development**: The application is developed as usual using the **Software Development Cycle**.
2.  **Containerization**: When ready for publication, the **Application is placed in a container**.
3.  **Deployment**: The container can then be deployed to **Azure Container Instances**.

### Service Highlights

1.  **User to Run Container Workloads**: ACI is the primary Azure service for running container workloads (processes or applications).
2.  **On-Demand = Save $$$**: Use containerized applications to process data on demand by only creating the container image when you need it, which helps save costs.
3.  **Works With Your Tool of Choice**: Manage ACI through the Azure Portal, Azure CLI, or PowerShell, catering to user preference.