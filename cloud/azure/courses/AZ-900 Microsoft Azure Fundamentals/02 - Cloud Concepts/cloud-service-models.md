# Cloud Service Models (IaaS, PaaS, SaaS, Serverless)

[⬆ Back to Parent](../02%20-%20Cloud%20Concepts/README.md)
[🏠 Back to Root README (../../../../../../README.md)

## Parent Context

This document is part of the "Cloud Concepts" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file provides a detailed explanation of the primary cloud service models: Infrastructure-as-a-Service (IaaS), Platform-as-a-Service (PaaS), Software-as-a-Service (SaaS), and Serverless computing. It includes key characteristics, benefits, examples, and the critical concept of the Shared Responsibility Model in cloud environments.

## Role in System

Understanding these service models is fundamental for choosing the right cloud services for specific application and business needs. This document helps in differentiating between models, comprehending their implications for management and responsibility, and making informed decisions about cloud adoption strategies.

## Key Cloud Service Models

### EXAM TIPS

**Service is the core of Azure, and there are three main ways to go about it.**

-   **IaaS**: Provides servers, storage, and networking as a service.
-   **PaaS**: A superset of IaaS, also including middleware such as database management tools.
-   **SaaS**: When a service is built on top of PaaS, like Office 365.
-   **Serverless**: You don't manage any servers; it allows a single function to be hosted, deployed, run, and managed on its own.

### Infrastructure-as-a-Service (IaaS)

-   Provides actual servers, storage, and networking as a service.
-   Scaling is fast.
-   No ownership of hardware.
-   **Model Characteristics**: Organization has complete control of the infrastructure, dynamic and flexible, cost varies depending on consumption, services are highly scalable, multiple users share a single piece of hardware.
-   **Examples**: VMs, VNets, Storage.

### Platform-as-a-Service (PaaS)

-   A superset of IaaS, including middleware such as database management tools.
-   Supports the web application life cycle.
-   Avoids software license management complexities.
-   **Model Characteristics**: Resources are virtualized and can easily be scaled up or down, services often assist with development, testing, and deployment of apps, multi-user access via the same development application, integrates web services and databases.
-   **Examples**: App Services, Azure CDN, Cosmos DB.

### Software-as-a-Service (SaaS)

-   Provides a fully managed service, accessible over the internet.
-   Users pay an access fee and are not responsible for hardware or software updates.
-   **Model Characteristics**: Managed from a central location, hosted on a remote server, accessible over the internet, users not responsible for hardware or software updates, often includes rate limiting/QoS.
-   **Examples**: Microsoft 365, Stripe (credit card payments), Gmail, QuickBooks.

### Serverless Computing

-   **Azure Functions** is an example of a serverless service.
-   Extreme PaaS: code is hosted, deployed, run, and managed without having to maintain a full application infrastructure.

## Shared Responsibility Model

A critical concept that clarifies who (Microsoft or the customer) is responsible for managing different aspects of the cloud environment depending on the cloud service model used.

-   ![Shared Responsibility Model](./images/srm.png)
