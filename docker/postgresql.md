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