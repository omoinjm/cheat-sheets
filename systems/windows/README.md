---
type: directory
path: systems/windows
parent: systems
tags: [repo, documentation, systems, windows]
---
# Windows Operating System

## 🔗 Navigation
- [⬆ Parent](./../README.md)
- [🏠 Root](./../../README.md)
- [📂 Current Directory](././)

## 📌 Overview
This directory contains documentation, configurations, and scripts specific to the Windows operating system. It serves as a centralized location for Windows-specific knowledge.

## 📁 Contents
- [macOSBigSur-Windows](./macOSBigSur-Windows/README.md): Information and files related to customizing Windows with macOS Big Sur aesthetics.

## 🧠 Responsibilities
This directory is responsible for holding all documentation related to the Windows operating system. It categorizes information to ensure that platform-specific guides, scripts, and configurations are easy to locate.

## 🔄 Relationships
This directory is a child of the [systems](./../README.md) directory. Its content provides Windows-specific instructions for developers and administrators.

## ✨ Useful Information

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
