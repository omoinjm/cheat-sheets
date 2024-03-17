# Setting up MYSQL on Docker

```bash
# Pull the image
docker pull mysql
```

```bash
docker run --name grooove-mysql \
-p 3306:3306 \
-e "MYSQL_ROOT_PASSWORD=<PASSWORD>" \
-d mysql:latest
```

```powershell
docker run --name grooove-mysql `
-p 3306:3306 `
-e "MYSQL_ROOT_PASSWORD=<PASSWORD>" `
-d mysql:latest
```

## Tags

- `-d`: To run our container detached in the background

- `-p`: Connect to the sql instance from the host/pc so we bind 1433 port on the container to the host/pc

- `-e`: Configure SQL Server using environment variables in the container

     `MYSQL_ROOT_PASSWORD=<PASSWORD>` - SQL Admin password

- `--name`: Give the container a name so we don't have to use the long Id given to us by default

- `mysql:latest`: name and tag of the conatainer image we want to use

## Connect to the SQL instance

- `Connection type`: MYSQL

- `Server`: loaclahost

- `Authentication type`: SQL Login

- `User name`: root

- `Password`: "`<Password>`"