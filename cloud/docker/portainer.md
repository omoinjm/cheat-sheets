### Docker Compose

```yaml
version: '3.3'
services:
  portainer-ce:
    ports:
      - '9000:9000'
      - '8000:8000'
    container_name: portainer
    networks:
      - nginxproxymanager_default
    restart: always
    volumes:
      - '/var/run/docker.sock:/var/run/docker.sock'
      - '/home/ubuntu/docker/portainer:/data'
    image: 'portainer/portainer-ce:latest'

networks:
  nginxproxymanager_default:
    external: true
```

```bash
# Run when done (detached)
docker-compose up -d
```