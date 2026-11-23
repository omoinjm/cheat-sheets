# Azure Resource Manager (ARM) Templates

[⬆ Back to Parent](../01%20-%20Introduction/README.md)
[🏠 Back to Root README (../../../../../../README.md)

## Parent Context

This document is part of the "Introduction to Azure" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file explains Azure Resource Manager (ARM) templates, a key feature for automating and managing Azure infrastructure. It covers the definition, key features, benefits, and provides an example of an ARM template.

## Role in System

ARM templates are central to Azure's Infrastructure as Code (IaC) capabilities. This document introduces how they enable consistent, repeatable, and automated deployment and management of Azure resources, significantly reducing manual errors and improving operational efficiency.

## Key Concepts

### Automate and Replicate Tasks, Actions, and Processes

ARM templates provide a structured and efficient way to describe resource usage within Azure environments. Whether you're updating, deleting, or creating resources, ARM templates offer a consistent approach.

### Key Features

-   **Resource Description**: Clearly articulate what resources are being manipulated within your Azure infrastructure.
-   **Common Syntax**: ARM templates utilize a defined language, streamlining the process and making it easier to formalize and learn.
-   **Idempotent**: Ensures that applying an ARM template multiple times yields the same result, promoting consistency and reliability.

By leveraging ARM templates, you can efficiently manage your Azure resources while maintaining consistency and reliability across deployments.

### Example ARM Template Structure

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "resources":[
        {
            "type": "Microsoft.Storage/storageAccounts",
            "apiVersion": "2019-04-01",
            "name": "{provide-unique-name}",
            "location": "eastus",
            "sku": {
                "name": "Standard_LRS"
            },
            "kind": "StorageV2",
            "properties":{
                "supportsHttps TrafficOnly": true
            }
        }
    ]
}
```

-   `$schema`: Defines the schema for the template.
-   `contentVersion`: Version of the template, indicating changes.
-   `resources`: Specifies the resources to create or manipulate.

### Benefits

-   **Idempotent**: Applying the same template multiple times produces the same outcome.
-   **Source Control**: Templates can be stored and versioned in source control.
-   **Reuse**: Combine multiple partial templates to build complex deployments.
-   **Declarative**: Specify the desired state of resources, not the steps to achieve it.
-   **No Human Errors**: Automation reduces manual configuration mistakes.