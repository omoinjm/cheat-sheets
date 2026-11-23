# Azure Regions and Availability Zones

[⬆ Back to Parent](../03%20-%20Azure%20Architecture/README.md)
[🏠 Back to Root README (../../../../../../README.md)

## Parent Context

This document is part of the "Azure Architecture" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file provides a comprehensive overview of Azure's global infrastructure, detailing the concepts of Azure Regions and Availability Zones. It explains their definitions, the criteria for choosing a region, the concept of paired regions, and the independent nature of availability zones.

## Role in System

Understanding Azure Regions and Availability Zones is fundamental for designing highly available, resilient, and geographically distributed applications on Azure. This document helps in making informed decisions about service deployment locations to meet latency, compliance, and disaster recovery requirements.

## Key Concepts

### Region Definition

An Azure Region consists of two or more data centers connected by a high-speed, low-latency network.

-   **A set of datacenters**: Each region comprises multiple physical data center locations.
-   **Latency defined perimeter**: Data centers within a region are geographically close to ensure low latency.
-   **Regional low-latency network**: A fiber connection links data centers within the region.

    ![Region Definition](./images/region-def.png)

### How to Choose a Region

Consider factors like service availability, data residency requirements, and proximity to users.

![Region Choice](./images/region-choice.png)

#### Paired Regions

Azure regions are generally paired within the same geographic area (with some exceptions like Brazil South) to support high availability and disaster recovery.

1.  **Each Region is Paired**: Most Azure regions have a pair.
2.  **Outage Failover**: Facilitates failover to the secondary region during an outage.
3.  **Planned Updates**: Ensures only one region in a pair is updated at any one time to minimize downtime.
4.  **Replication**: Some services use paired regions for data replication.

### Availability Zones

Availability Zones are physically separate locations within an Azure region.

-   **Physical Location**: Each zone is a distinct physical location.
-   **Independent**: Each zone has its own independent power, cooling, and networking.
-   **Zones**: Each region that supports Availability Zones has a minimum of three separate zones.
