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
3. Create NGINX config file

  - We're gonna add configurations to different sites in the `/etc/nginx/sites-available/{name-of-project}` folder then create a symbolic link pointing to `/var/www/{name-of-project}`

```bash
   server {
        listen 80;
        server_name www.my-domain.com my-domain.com;

        gzip on;
        gzip_proxied any;
        gzip_types application/javascript application/x-javascript text/css text/javascript;
        gzip_comp_level 6;
        gzip_buffers 16 8k;
        gzip_min_length 256;

        location /_next/static/ {
                alias /var/www/new-site-nextjs/.next/static;
                expires 365d;
                access_log off;
        }
        
        location / {
                proxy_pass http//127.0.0.1:3000;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
   }
```
