# Resource Groups & Azure Resource Manager

Resource groups are containers that hold related resources for an azure solution and includes those resources that you want to manage as a group.

## Resource Groups Facts

**One Resource**: Each resource can only exist in a single resource group.

**Add/Remove**: You can add or remove resources to any resource group at any time.

**Move Resource**: You can move a resource from one resource group to another.

**Multiple Regions**: Resources from multiple regions can be in one resource group.

**Access Control**: You can give users access to a resource group and everything in it.

**Interact**: Resources can interact with other resources in different resource groups.

**Location**: A resource group has a location, or region, as it stores meta data about the resources in it.


## Azure Resource Manager (ARM)

This is the under-pinning of everythin on azure when it comes to creating, removing, updating or deleting resources. It is deployment and management services on azure.

All resources go through ARM. Portal, Powershell, Azure CLI, REST API's or client SDK's - ARM handles all these request.

### ARM Benefits

![alt text](./images/arm-benefits.png)

## Summary

**Resource Groups**:

- All resources belong to a resource group. It isn't a resource, but helps structure your Azure architecture.

**Azure Resource Manager**:

- All interaction with Azure resources go through the ARM.

- It is the main Azure Architecture component for creating, updating and manipulating resources.