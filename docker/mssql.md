# Run SQL Server in a Docker Container

## Command

```bash
docker run -d \
-p 1433:1433 \
-e "ACCPET_EULA=Y" \
-e "SA_PASSWORD=<PASSWORD>" \
-v ~/Documents/SQLMount:/SQLMount \
--name docker-mssql \
mcr.microsoft.com/mssql/server:2019-latest
```

```powershell
docker run -d `
-p 1433:1433 `
-e "ACCPET_EULA=Y" `
-e "SA_PASSWORD=<PASSWORD>" `
-v ~/Documents/SQLMount:/SQLMount `
--name docker-mssql `
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
