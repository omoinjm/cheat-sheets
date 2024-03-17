# Setting up Nginx Proxy Manager

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped # Policy (if something goes wrong)
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
      # - '9443:9443' # portainer
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```

```bash
# Run when done (detached)
docker-compose up -d
```