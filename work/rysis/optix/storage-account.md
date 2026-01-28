# Optix - Azure Storage Account Access Script (`storage-account.md`)

[⬆ Back to Parent](../optix/README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This document is part of the "Optix" component documentation within the Rysis project, focusing on integration with Azure storage solutions.

## Contents Overview

This file provides a PowerShell script designed to connect to an Azure Storage Account (specifically a File Share) by mounting it as a network drive. The script first tests network connectivity to the storage account via port 445 (SMB) and then uses `cmdkey` to persist credentials and `New-PSDrive` to create a persistent mapped drive. It also includes error handling for connectivity issues.

## Role in System

This script is crucial for developers and operations teams who need to access Azure File Shares from Windows environments for tasks such as data exchange, configuration management, or log collection within the Optix ecosystem. It automates the process of establishing a reliable connection to cloud storage resources.

## PowerShell Script for Storage Account Access

The following PowerShell script allows you to connect to an Azure Storage Account File Share.

```powershell
$connectTestResult = Test-NetConnection -ComputerName stoptixewbot.file.core.windows.net -Port 445

if ($connectTestResult.TcpTestSucceeded) {
    # Save the password so the drive will persist on reboot
    cmd.exe /C "cmdkey /add:`"stoptixewbot.file.core.windows.net`" /user:`"localhost\stoptixewbot`" /pass:`"FxnnA/XCgHxsYVNnX6jUQxpHoI6Qnm0XuzK4irwIpM3IKp9vlPZwqAeB12aOE1wn0SBc/Nylm8mD+ASt16vipQ==`""
    # Mount the drive
    New-PSDrive -Name L -PSProvider FileSystem -Root "\\stoptixewbot.file.core.windows.net\share1" -Persist
} else {
    Write-Error -Message "Unable to reach the Azure storage account via port 445. Check to make sure your organization or ISP is not blocking port 445, or use Azure P2S VPN, Azure S2S VPN, or Express Route to tunnel SMB traffic over a different port."
}
```

## Key Script Functionality

-   **`Test-NetConnection`**: Checks for successful TCP connectivity to the Azure storage account endpoint on port 445.
-   **`cmdkey /add`**: Persists the credentials for the storage account in the Windows credential manager, ensuring the drive remains mapped after reboots.
-   **`New-PSDrive -Persist`**: Creates a new persistent mapped network drive (`L:`) to the specified Azure File Share (`\\stoptixewbot.file.core.windows.net\share1`).
-   **Error Handling**: If port 445 is blocked, it provides guidance on troubleshooting connectivity issues, suggesting VPN or ExpressRoute alternatives.

## Usage Notes

-   Replace `stoptixewbot.file.core.windows.net`, `localhost\stoptixewbot`, `FxnnA/XCgHxsYVNnX6jUQxpHoI6Qnm0XuzK4irwIpM3IKp9vlPZwqAeB12aOE1wn0SBc/Nylm8mD+ASt16vipQ==` (storage account key), and `share1` with your actual Azure Storage Account name, username, key, and file share name respectively.
-   Ensure port 445 (SMB) is open on your network or use the suggested alternatives for connectivity.