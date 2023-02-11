# SETUP NGINX SERVER

Deploy Node js webapp to ubuntu server

### Create new user with root permissions and SSH access.
   
   - Doing this for safey precausions
   - Use sudo commands for root priviledges
   - Make sure you're running as `root` user for this process
     
     ```bash
     adduser {username}
     
     # Enter password
     # The other options you can ignore
     # e.g, Full Name, Room Number etc...
     ```
   
   1. Give the user root access
     
      ```bash
      usermod -aG sudo {username}
      ```
   
   2. Give `ssh` access for this user
     
      ```bash
      # 1. First create a `.ssh` folder in users home directory
      mkdir /home/{username}/.ssh
     
      # 2. Copy the authorized keys into this newly created folder
      cp /root/.ssh/authorized_keys /home/{username}/.ssh/authorized_keys
     
      # 3. Chnage user permissions of .ssh folder from `root` to `{username}`
      chown -R {usernmae}:{username} .ssh
      ```
   
   3. Setup permissions of this file/folder, so as to avoid the file from being tampered with

      ```bash
      cd /home/{username}/
      
      # Read Write and Execute this folder but only for this user
      chmod 700 .ssh
      ```
     
      ```bash
      cd .ssh
      
      # Do the same thing for the authorized_keys file
      # 600 means our newly createsd user is going to have Read and Write permissions
     
      chmod 600 authorized_keys
      ```
   
   4. Allow the firewall to flow through the ssh port
       
      ```bash
      # Allow access on port 22
      ufw allow 22
      
      # Allow incoming TCP connections on port 22 from IP address {ip-address}
      sudo ufw allow from {ip-address} to any port 22 proto tcp


      # Enable firewall to make sure hackers don't access our server via other ports
      ufw allow OpenSSH

      ufw enable
      ```
     
   5. Exit server and connect using new user
     
      ```bash
      ssh {username}@{public_ip}
      ```
   
   6. Secure server
   
      ```bash
      # We edit this file in order to disable password access to the server.
      # This is secure because we can only access the server via ssh using a public key.
      # Hackers won't be able to brute force their way into this server.
      # Also we have to disable root access to our server.
     
      sudo vim /etc/ssh/sshd_config
     
      # Change `PermitRootLogin no`
      # Chnage `PasswordAuthentication no`
      ```
     
   7. Restart server services
     
      ```bash
      sudo systemctl restart ssh
      sudo systemctl restart sshd
      ```

### Install packages:
   
   - `nginx` to server application publically
   - `certbot` to generate free ssl certificate
   - `python3-cervot-nginx` script that allows us to interact with cerbot let encrpt and nginx. it is going to allow for automatic redirect
     
     ```bash
     # Update and upgrade system with apt
     sudo apt update && sudo apt upgrade
     
     # Install packages
     sudo apt install nginx certbot python3-cervot-nginx
     ```
         
### Create NGINX config file

   - Remove `/etc/nginx/sites-enabled/default` to prevent any conflicts.
      
     ```bash
     # -f for force, -r for recursively
     rm -rf /etc/nginx/sites-enabled/default
     # OR
     sudo unlink /etc/nginx/sites-enabled/default
     ```
      
   - Add configurations to different sites in the `/etc/nginx/sites-available/{name-of-project}` folder then create a symbolic link pointing to `/var/www/{name-of-project}`
   
   - Create config file
     ```bash
     sudo vim /etc/nginx/sites-available/{name-of-project}
     ```
   
     ```bash
     server {
            
            listen 80;
            
            # Rename folders/files /var/www/{name-of-prohect}, /etc/nginx/sites-available/{name-of-project} and /etc/nginx/sites-enabled/{name-of-project} to be the same as your `server_name`
            server_name www.example.com;
            
            proxy_buffers 8 16k;
            proxy_buffer_size 32k;

            client_body_buffer_size 10K;
            client_header_buffer_size 1K;
            client_max_body_size 8M;

            keepalive_timeout 65;

            gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
             
            location /_next {
                    alias /var/www/{name-of-project}/.next;
                    expires 365d;
                    proxy_buffering on;
                    # disable access log.
                    # we don't want to keep things like javascript, css and image.
                    access_log off;
                    proxy_cache_valid 200 60m;
            }

            location / {
                    # need to research these
                    # If find errors follow:
                    # https://stackoverflow.com/questions/51972426/is-there-a-way-to-make-nginx-terminate-a-websocket-connection-and-pass-only-the
                    # https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass
                    proxy_pass http://127.0.0.1:3000;
                    proxy_http_version 1.1;

                    # handle web socket connections.
                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection 'upgrade';
                    proxy_set_header Host $host;
                    proxy_cache_bypass $http_upgrade;
            }
     }
     ```
   
   - Create a symboic link
    
     ```bash
     sudo ln -s /etc/nginx/sites-available/{name-of-project} /etc/nginx/sites-enabled/{name-of-project}
     ```

### Restart `nginx` with `systemctl`
 
   ```bash
   sudo systemctl restart nginx
   # Test if nginx config is good
   sudo nginx -t
   ```
   
   - Clone your project under `/var/www/`
      
     ```bash
     git clone {project-url}
     ```

   - Change permissions to readonly

     ```bash
     sudo chown -R user:user {name-of-project}
     ```
   
### Allow our firewall to receive connections via port 80 and 433
  
   - Which are the ports we're allowed to connect to with out a `SSL` certificate
   - We also want to redirect from http to https

     ```bash
     sudo ufw allow "Nginx Full"

     # View Status
     sudo ufw status
     ```

### Install node, nvm and pm2
    
   - link: https://github.com/nvm-sh/nvm

     ```bash
     cd ~
    
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    
     # Refresh shell (allow newly installed packages to be accessable)
     exec $SHELL
    
     # Install latest stable features
     nvm install --lts
     
     # Install yarn and pm2
     npm i -g yarn pm2
     ```

### Clone project from repo and set user as owner

   - Clone in `/var/www/`
     
     ```bash
     git clone {name-of-project}
     ```
      
   - Change permission of folder so that our user can have access

     ```bash
     # -R for recursive
     sudo chown -R omoi:omoi /var/www/{name-of-project}
     ```
     
### Go to `/var/www/{name-of-project}`

   ```bash
   yarn install
   # OR
   npm install
    
   yarn run build
   # OR
   npm run build
   ```
    
### Start project in the background with pm2
   
   - Tell pm2 to run our project using yarn
   
     ```bash
     pm2 start yarn --name {name-of-project} -- start
     ```
    
   - Bugs: if pm2 doesn't run
   
     ```bash
     # terminate project as a process
     pm2 stop {name-of-project}
     
     # deletes project as a process
     pm2 delete {name-of-project}
     
     # run project as a process
     pm2 start yarn --name {name-of-project} -- start
     ```

### Install Let's Encrypt SSL certificate with certbot
   
   ```bash
   cd /var/www/{name-of-project}
   
   # Generates free SSL certificate provided by https://letsencrypt.org
   sudo certbot --nginx -d {doamin-name}
   
   # You'll be prompted to enter email
   # and Aggree to their terms of service
   # and recieve newsletter marketing emails
   # Select 2) Redirect
   ```
