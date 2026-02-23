# LAMP Server Setup Script (`setup_lamp_server.sh`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the server creation automation tools within the Linux operating system documentation.

## Contents Overview

The `setup_lamp_server.sh` script automates the installation and basic configuration of a LAMP (Linux, Apache, MySQL, PHP) server stack on an Ubuntu Virtual Machine. It updates the package manager, installs Apache2, MySQL Server, and PHP with its Apache module and MySQL extension. It also includes steps to restart Apache, secure MySQL, and test the PHP installation.

## Role in System

This script provides a rapid and consistent way to provision a development or production-ready LAMP server. It significantly reduces the manual effort and potential for errors associated with setting up a web server environment, making it ideal for deploying PHP-based applications.

## Usage

This script is designed to be run on a newly provisioned Ubuntu VM. It assumes SSH access to the VM.

```bash
# First, connect to your VM
ssh azureuser@omoiseeker

# Then, execute the script
./setup_lamp_server.sh
```

### Script Logic

1.  **Connect to VM**: (Assumed an `ssh` command, but the script itself runs commands *on* the connected VM).
2.  **Update Packages**: `sudo apt-get update`
3.  **Install Apache2**: `sudo apt-get install apache2 -y`
4.  **Install MySQL Server**: `sudo apt-get install mysql-server -y`
5.  **Install PHP**: `sudo apt-get install php libapache2-mod-php php-mysql -y`
6.  **Restart Apache**: `sudo service apache2 restart`
7.  **Secure MySQL**: `sudo mysql_secure_installation` (This step will require interactive user input).
8.  **Test PHP**: Creates a `info.php` file in `/var/www/html` to verify PHP installation.

## Entry Points

-   Execution: `./setup_lamp_server.sh` on the target Ubuntu VM.
-   Interactive input: `sudo mysql_secure_installation` requires user interaction.

## Conventions

-   Assumes Ubuntu Linux distribution.
-   Requires `sudo` privileges for package installations and service management.
-   Assumes `ssh` client is available on the local machine to connect to the VM.
