#!/bin/bash

# Connect to the VM
ssh azureuser@omoiseeker

# Update the package manager
sudo apt-get update

# Install Apache web server
sudo apt-get install apache2 -y

# Install MySQL server
sudo apt-get install mysql-server -y

# Install PHP
sudo apt-get install php libapache2-mod-php php-mysql -y

# Restart Apache to enable PHP
sudo service apache2 restart

# Secure MySQL server
sudo mysql_secure_installation

# Test PHP
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php