# Language of Cloud Computing

[⬆ Back to Parent](../02%20-%20Cloud%20Concepts/README.md)
[🏠 Back to Root README (../../../../../../README.md)

## Parent Context

This document is part of the "Cloud Concepts" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file defines and explains key terminology used in cloud computing, such as High Availability, Reliability (Fault Tolerance/Disaster Recovery), Scalability (Horizontal vs. Vertical), Predictability (Performance and Costs), Security, Governance, and Manageability. These concepts are fundamental to understanding the benefits and operational aspects of cloud environments.

## Role in System

A clear understanding of these terms is essential for anyone working with cloud technologies. This document clarifies the core language of cloud computing, enabling effective communication, design, and management of cloud resources within Azure and other platforms.

## Key Concepts and Terms

### EXAM TIPS

Cloud computing has specific and critical terms for understanding its principles.

### Resilience

The ability of a system to recover from failures and continue to function.

-   **High Availability**: Systems are always available, often with automatic failover.
    -   *Traditional vs. Cloud*: Cloud environments offer significant advantages in quickly replacing failed hardware and using clusters for continuous availability.
-   **Reliability (a.k.a. Fault Tolerance/Disaster Recovery)**: Azure's capability to tolerate failures or even disasters.
    -   Achieved by deploying resources in multiple locations (global-scale computing) and ensuring no single point of failure.

### Scalability

Automatically adjust resources (horizontally or vertically) to meet demand.

-   **Horizontal vs. Vertical Scaling**:
    | Horizontal                           | Vertical                                          |
    | :----------------------------------- | :------------------------------------------------ |
    | Adding additional VMs/containers.    | Increasing power (e.g., CPU/RAM) of existing VMs. |
    | Scaling out.                         | Scaling up.                                       |
    -   Emphasis on not overpaying for services and automatically reducing resources when demand drops.

### Predictability

Ensuring consistent performance for users and predictable costs.

-   **Performance**: Consistent user experience regardless of traffic, supported by autoscaling, load balancing, and high availability.
-   **Costs**: Tracking and forecasting resource usage in real-time to avoid unexpected expenses.

### Management

-   **Security**: Full control over your cloud security posture, including patches, maintenance, and network control.
-   **Governance**: Standardizing cloud deployments to meet regulatory requirements and company standards.
-   **Manageability**: Efficient management of cloud resources through various tools and approaches.
    -   *Management of the cloud*: Autoscaling, Monitoring, Template-based deployments.
    -   *Management in the cloud*: Portal, CLI, APIs.