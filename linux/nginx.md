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

        # gzip allows us to compress our static files.
        # it is great for speed and ranking higher on google
        gzip on;
        
        # we're using a proxy server so this allows for gzip to be enabled.
        # we'll use pm2 to run our website as a background service.
        # this process will proxy our website into the internet.
        gzip_proxied any; 
        
        # this will make sure all our javascript and css files are all compressed.
        gzip_types application/javascript application/x-javascript text/css text/javascript;
        
        # sets the compression level. This is a value set bewtween 1 and 9.
        # each time we compress/decompress out files it'll take some processing power.
        # we need to find a perfect balance between that processing power and file compression/decompression so that we don't get a large file size.
        gzip_comp_level 6;
        
        # need to research
        gzip_buffers 16 8k;
        
        # make sure to not compress files that are too small.
        # the aim is to use less processing power
        gzip_min_length 256;

        # 
        location /_next/static/ {
                alias /var/www/{name-of-project}/.next/static;
                expires 365d;
                
                # disable access log.
                # we don't want to keep things like javascript, css and image.
                access_log off;
        }
        
        location / {
                proxy_pass http//127.0.0.1:3000;
                proxy_http_version 1.1;
                
                # handle web socket connections.
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
   }
```

  - Remove `/etc/nginx/sites-enabled/default` to prevent any conflicts.
  
  - Create symbolic link
    
    ```bash
     sudo ln -s /etc/nginx/sites-available/{name-of-project} /etc/nginx/sites-enabled/{name-of-project}
    ```

  - Restart `nginx` with `systemctl`
    ```bash
    sudo systemctl restart nginx
    ```
    
  - Clone your project under `/var/www/`

  - Change permissions to readonly
    ```bash
    sudo chown -R user:user {name-of-project}
    ```
  - Allow our firewall to receive connections via port 80 and 433
  
