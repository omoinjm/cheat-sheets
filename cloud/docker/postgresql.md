# Run PostgreSQL in a Docker Container

## Command

```bash
# Pull the image
docker pull postgres
```

```bash
docker run --name grooove-postgresql \
-p 5432:5432 \
-e "POSTGRES_PASSWORD=<PASSWORD>" \
-d postgresql:latest
```

```powershell
docker run --name grooove-postgresql `
-p 5432:5432 `
-e "POSTGRES_PASSWORD=<PASSWORD>" `
-d postgres:latest
```

## Backup / Restore database

Here is a step-by-step guide: [link](https://www.tecmint.com/backup-and-restore-postgresql-database/)

```bash
sudo pg_dump --dbname=NAME --username=USER > grooove_bak.sql
```

### Docker Compose

```yaml
version: '3.8'
services:
  db:
    container_name: postgres_container
    image: postgres:latest
    restart: always
    ports:
      - "5432:5432"
    volumes:
            - db:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres

  pg-admin:
    container_name: pgadmin4_container
    image: dpage/pgadmin4
    restart: always
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  db:
    driver: local
```

```bash
# Run when done (detached)
docker-compose up -d
```