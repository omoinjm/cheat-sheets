# Windows Operating System

[⬆ Back to Parent](../os/README.md)
[🏠 Back to Root README](../../README.md)

## Contents Overview

This directory contains documentation and tips specific to the Windows operating system.

### Subdirectories

-   [macOSBigSur-Windows](./macOSBigSur-Windows/README.md): Information and files related to customizing Windows with macOS Big Sur aesthetics.

### Files

-   `README.md`: This file, providing an overview of Windows-related documentation.

## Role in System

This section serves as a centralized location for Windows-specific knowledge, configurations, and useful command-line snippets. It helps in quickly referencing solutions for common Windows tasks and customization.

## Useful Information

### Load macOS Big Sur Cursors

To load the macOS Big Sur cursors:
1.  Right-click the `install.inf` file within the `macOSBigSur-Windows` directory and select "Install".
2.  Open "Control Panel" -> "Mouse" (or type `control mouse` in `Win + R`).
3.  Under the "Pointers" tab, change the scheme to "macOSBigSur".

### Environment Variables

Refer to the external resource for setting environment variables: [Set Environment Variables](https://www.devdungeon.com/content/set-environment-variables-windows)

### Hide Files (PowerShell)

To hide file content within another file using PowerShell:

```powershell
# Hide file content within another file; delete original file after
type file > demoFile:file

# View contents
cat demoFile:file

# Show hidden files in an alternate data stream
dir /r
```

Another method (checks "show/hide hidden files" option in Folder Options):

```powershell
attrib +h file
```

### Setup SSH on Personal Laptop

Refer to the external resource for setting up SSH on Windows: [Setup for Windows](https://theitbros.com/ssh-into-windows/)