# Run SQL Server in a Docker Container

## Command

```bash
# Create a volume
docker volume create docker-mssql-data
```

```bash
docker run -d \
-p 1435:1433 \
-e "ACCEPT_EULA=Y" \
-e "SA_PASSWORD=<PASSWORD>" \
--name docker-sqlserver-2019 \
--mount source=docker-mssql-data,target=/var/opt/mssql \
mcr.microsoft.com/mssql/server:2019-latest

# Alternatively without creating a volume (keeps data persistent on local machine)
docker run -d \
-p 1433:1433 \
-e 'ACCEPT_EULA=Y' \
-e 'MSSQL_SA_PASSWORD=<PASSWORD>' \
-v '/mnt/d/omoi/data/docker/volumes/data':/var/opt/mssql/data \
-v '/mnt/d/omoi/data/docker/volumes/log':/var/opt/mssql/log \
-v '/mnt/d/omoi/data/docker/volumes/secrets':/var/opt/mssql/secrets \
--name sqlserver-2019 \
mcr.microsoft.com/mssql/server:2019-latest
```

```powershell
docker run -d `
-p 1435:1433 `
-e "ACCEPT_EULA=Y" `
-e "SA_PASSWORD=<PASSWORD>" `
--name docker-mssql `
--mount source=docker-mssql-data,target=/var/opt/mssql `
mcr.microsoft.com/mssql/server:2019-latest
```

## Tags

- `-d`: To run our container detached in the background

- `-p`: Connect to the sql instance from the host/pc so we bind 1433 port on the container to the host/pc

- `-e`: Configure SQL Server using environment variables in the container

  `ACCPET_EULA=Y` (EULA meaning End User License Agreement) - This just tells SQL Server as it starts up that we accpect the license agreement

  `SA_PASSWORD=<PASSWORD>` - SQL Admin password

- `-v`: We want to be able to access files on the host/pc from within the container. We mount a volume to do this

- `--name`: Give the container a name so we don't have to use the long Id given to us by default

- `mcr.microsoft.com/mssql/server:2019-latest`: name and tag of the conatainer image we want to use

## Connect to the SQL instance

- `Connection type`: Microsoft SQL Server

- `Server`: loaclahost

- `Authentication type`: SQL Login

- `User name`: sa

- `Password`: "`<Password>`"

## Docker Compose

Create `docker-compose.yml` and `dockerfile` files:

To rebuild this image you must use `docker-compose build` or `docker-compose up --build`

```yaml
version: '3.8'
services:
  identity-database:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      - "1433:1433"
    env_file:
      - MSSQL_SA_PASSWORD=<sql-server-admin-password>
      - ACCEPT_EULA=Y
      - MSSQL_DATA_DIR=/var/opt/sqlserver/data
      - MSSQL_LOG_DIR=/var/opt/sqlserver/log
      - MSSQL_BACKUP_DIR=/var/opt/sqlserver/backup
    volumes:
      - sqlsystem:/var/opt/mssql/
      - sqldata:${MSSQL_DATA_DIR}
      - sqllog:${MSSQL_LOG_DIR}
      - sqlbackup:${MSSQL_BACKUP_DIR}
volumes:
  sqlsystem:
  sqldata:
  sqllog:
  sqlbackup:
```

```dockerfile
# build from the Ubuntu 18.04 image
FROM ubuntu:20.10
 
# create the mssql user
RUN useradd -u 10001 mssql
 
# installing SQL Server
RUN apt-get update && apt-get install -y wget software-properties-common apt-transport-https
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/18.04/mssql-server-2019.list)"
RUN apt-get update && apt-get install -y mssql-server
 
# creating directories
RUN mkdir /var/opt/sqlserver
RUN mkdir /var/opt/sqlserver/data
RUN mkdir /var/opt/sqlserver/log
RUN mkdir /var/opt/sqlserver/backup
 
# set permissions on directories
RUN chown -R mssql:mssql /var/opt/sqlserver
RUN chown -R mssql:mssql /var/opt/mssql
 
# switching to the mssql user
USER mssql
 
# starting SQL Server
CMD /opt/mssql/bin/sqlservr
```

```bash
# Run when done (detached)
docker-compose up -d
```