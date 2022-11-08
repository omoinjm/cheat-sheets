# Useful Links

## **LINUX**

- Install the .NET SDK or the .NET Runtime on Ubuntu

  link: https://docs.microsoft.com/en-us/dotnet/core/install/linux-ubuntu?source=recommendations#2004

- Set up an SSH key

  link: https://support.atlassian.com/bitbucket-cloud/docs/set-up-an-ssh-key/

- Permanently authenticating with Git repositories

  link: https://confluence.atlassian.com/bitbucketserver/permanently-authenticating-with-git-repositories-776639846.html

- How to make files accessible only by root?
  
  link: https://askubuntu.com/questions/193055/how-to-make-files-accessible-only-by-root

  ```bash
  sudo chown root:root /path/to/application
  ```

  ```bash
  sudo chmod 700 /path/to/application
  ```

 - How to Install OpenVPN in Ubuntu 20.04?

   link: https://www.tecmint.com/install-openvpn-in-ubuntu/

## **SQL**

  - Rename Tables (Database Engine)
    
    link: https://docs.microsoft.com/en-us/sql/relational-databases/tables/rename-tables-database-engine?view=sql-server-ver16
   
  - Rename Column
    
    link: https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-rename-transact-sql?redirectedfrom=MSDN&view=sql-server-ver16
    
  - DROP TABLE (Transact-SQL)

    link: https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-table-transact-sql?view=sql-server-ver16

## **OSINT Phone Number**

  - links: https://sundowndev.github.io/phoneinfoga/getting-started/install/
  
  - download: docker pull sundowndev/phoneinfoga:latest
  
  - version: docker run --rm -it sundowndev/phoneinfoga version
  
  - run terminal: docker run --rm -it sundowndev/phoneinfoga scan -n <number>
  
  - web ui: docker run --rm -it -p 8080:8080 sundowndev/phoneinfoga serve -p 8080
