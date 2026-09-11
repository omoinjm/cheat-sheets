# Create Azure Ubuntu VM Script (`create_aws_ubuntu_vm.sh`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the server creation automation tools within the Linux operating system documentation.

## Contents Overview

**Note:** Despite its filename, this script uses `az` commands, indicating it is designed for **Azure**, not AWS.

The `create_aws_ubuntu_vm.sh` script automates the provisioning of an Ubuntu Virtual Machine on **Microsoft Azure**. It handles the creation of a resource group, virtual network, public IP address, subnet, network interface card, and finally, the Ubuntu VM itself. It also generates SSH keys for access.

## Role in System

This script provides a quick and repeatable way to deploy a new Ubuntu VM instance in Azure. It is particularly useful for setting up development environments, testing servers, or components of a larger Azure-based infrastructure with minimal manual intervention.

## Usage

To use this script, you need to have the Azure CLI (`az`) installed and configured with appropriate credentials.

```bash
./create_aws_ubuntu_vm.sh
```

### Script Logic

1.  **Define Variables**: Sets `resource_group_name`, `vm_name`, and `location`.
2.  **Create Resource Group**: `az group create`
3.  **Create Network Resources**: `az network vnet create`, `az network public-ip create`, `az network vnet subnet create`, `az network nic create`.
4.  **Create Virtual Machine**: `az vm create` with specified image (`UbuntuLTS`), admin username, and SSH key generation.

## Entry Points

-   Execution: `./create_aws_ubuntu_vm.sh`
-   Dependencies: Azure CLI (`az`) must be installed and authenticated.

## Conventions

-   Uses `az` commands for Azure resource management.
-   Assumes default settings for many Azure resources, but can be customized by modifying the script variables.
-   Generates SSH keys for the `azureuser` admin account.
