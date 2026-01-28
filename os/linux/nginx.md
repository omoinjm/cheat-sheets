# Nginx Server Setup and Node.js Deployment

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../README.md)

## Parent Context

This document is part of the Linux operating system documentation, providing a comprehensive guide for deploying web applications using Nginx on an Ubuntu server.

## Contents Overview

This file details the process of setting up an Nginx server, creating secure user accounts, configuring SSH access, installing necessary packages (Nginx, Certbot), setting up Nginx configurations for Node.js applications, managing firewalls, and deploying Node.js applications with `nvm`, `yarn`, `pm2`, and securing them with Let's Encrypt SSL certificates.

## Role in System

This guide is crucial for deploying and managing web applications on Linux servers, providing a step-by-step approach to secure server setup, efficient web serving with Nginx, and automated SSL certificate management.

## Key Setup Steps and Commands

### Create New User with Root Permissions and SSH Access

This section emphasizes creating a dedicated user for security, granting `sudo` privileges, and configuring SSH access using public keys while disabling password authentication and root login.

**Key Commands:**
-   `adduser {username}`: Create a new user.
-   `usermod -aG sudo {username}`: Grant sudo access.
-   SSH directory and `authorized_keys` setup with correct permissions (`chmod 700 .ssh`, `chmod 600 authorized_keys`).
-   `sudo vim /etc/ssh/sshd_config`: Disable `PermitRootLogin` and `PasswordAuthentication`.
-   `sudo systemctl restart ssh` / `sudo systemctl restart sshd`: Restart SSH services.

### Install Packages

Install Nginx, Certbot, and the Nginx Certbot plugin for SSL certificate management.

**Key Commands:**
-   `sudo apt update && sudo apt upgrade`
-   `sudo apt install nginx certbot python3-certbot-nginx`

### Create NGINX Config File

Configure Nginx as a reverse proxy for your Node.js application, including proxy buffering, header settings, and static file serving.

**Key Commands:**
-   `rm -rf /etc/nginx/sites-enabled/default`: Remove default Nginx config.
-   `sudo vim /etc/nginx/sites-available/{name-of-project}`: Create new site configuration.
-   `sudo ln -s /etc/nginx/sites-available/{name-of-project} /etc/nginx/sites-enabled/{name-of-project}`: Create symbolic link to enable the site.
-   `sudo systemctl restart nginx` / `sudo nginx -t`: Restart Nginx and test configuration.

### Firewall Configuration

Allow necessary HTTP/HTTPS traffic through the firewall.

**Key Commands:**
-   `sudo ufw allow "Nginx Full"`
-   `sudo ufw status`

### Install Node, NVM, and PM2

Set up the Node.js environment and a process manager for your application.

**Key Commands:**
-   NVM installation via `curl`.
-   `nvm install --lts`: Install latest LTS Node.js.
-   `npm i -g yarn pm2`: Install Yarn and PM2 globally.

### Deploy and Start Application

Clone your project, install dependencies, build, and start it with PM2.

**Key Commands:**
-   `git clone {project-url}` into `/var/www/`.
-   `sudo chown -R user:user {name-of-project}`: Change project ownership.
-   `yarn install` / `npm install`
-   `yarn run build` / `npm run build`
-   `pm2 start yarn --name {name-of-project} -- start`: Start application with PM2.

### Install Let's Encrypt SSL Certificate with Certbot

Secure your Nginx site with a free SSL certificate.

**Key Commands:**
-   `sudo certbot --nginx -d {domain-name}`