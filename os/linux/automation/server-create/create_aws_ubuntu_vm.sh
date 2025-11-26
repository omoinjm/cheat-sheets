#!/bin/bash

# Set variables for resource group, VM name, and location
resource_group_name="demo-learning"
vm_name="omoiseeker"
location="westus2"

# Create a resource group
az group create --name $resource_group_name --location $location

# Create a virtual network and a public IP address
az network vnet create --resource-group $resource_group_name --name "myVnet" --address-prefixes "10.0.0.0/16"
az network public-ip create --resource-group $resource_group_name --name "myPublicIP"

# Create a subnet
az network vnet subnet create --resource-group $resource_group_name --vnet-name "myVnet" --name "mySubnet" --address-prefix "10.0.1.0/24"

# Create a virtual network card and associate with public IP address and subnet
az network nic create --resource-group $resource_group_name --name "myNic" --vnet-name "myVnet" --subnet "mySubnet" --public-ip-address "myPublicIP"

# Create the VM
az vm create --resource-group $resource_group_name --name $vm_name --location $location --nics "myNic" --image "UbuntuLTS" --admin-username "azureuser" --generate-ssh-keys