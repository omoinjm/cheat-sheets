---
title: Azure Functions (Serverless Compute)
description: An introduction to Azure Functions, covering serverless architecture, image processing use cases, and key benefits.
type: content
path: infrastructure/cloud/azure/courses/AZ-900 Microsoft Azure Fundamentals/04 - Compute/functions.md
tags: [infrastructure, cloud, azure, az-900, compute, serverless, functions]
---
# Azure Functions (Serverless Compute)

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../../../../../../README.md)

## Parent Context

This document is part of the "Compute Services" module within the AZ-900 Microsoft Azure Fundamentals course.

## Contents Overview

This file introduces Azure Functions, Azure's serverless compute offering. It explains the underlying architecture, illustrates a practical use case for image processing, and highlights the key benefits of using Functions for event-driven, scalable workloads.

## Role in System

Azure Functions enable developers to execute small pieces of code (functions) in the cloud without needing to provision or manage infrastructure. This document helps in understanding how Functions support a serverless architecture, reducing operational overhead and optimizing costs for specific, event-driven tasks.

## Key Concepts and Features

### Architecture

-   Azure Functions run on virtual machines in the background for computation.
-   Users experience **no maintenance**, **no processes**, and **nothing VM-related** to manage.
-   The focus is entirely on your application's functionality.

    ![Azure Functions Architecture](./images/azure-functions.png)

### Use Case: Image Processing

Imagine a business that allows users to upload pictures of their pets:

1.  These images need processing to optimize them for web display and storage.
2.  When a user uploads an image to your website, an `Azure Function` receives that image.
3.  The `Function`'s job is to process the image: compress it and change it to the correct file format.
4.  The `Function` then stores the processed image in a database for future use in your online application.

### Benefits

Azure Functions provide several significant advantages for modern application development:

-   ![Functions Benefits](./images/function-benefits.png)
