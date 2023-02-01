# SETUP NGINX SERVER

1. Install packages:
  
  - `nginx` to server application publically
  - `certbot` to generate free ssl certificate
  - `python3-cervot-nginx` script that allows us to interact with cerbot let encrpt and nginx. it is going to allow for automatic redirect

2. Create website folder and set user as owner

  - Create a folder under `/var/www/{name-of-project}`
  - Change permission of folder so that our user can have access
    ```bash
    # -R for recursive
    sudo chown -R omoi:omoi /var/www/{name-of-project}
    ```
3. Create NGINE config file

  - We're gonna add configurations to different sites in the `/etc/nginx/sites-available/{name-of-project}` folder then create a symbolic link pointing to `/var/www/{name-of-project}`
