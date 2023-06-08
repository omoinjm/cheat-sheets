# **SQL**

  - Rename Tables (Database Engine)
    
    link: https://docs.microsoft.com/en-us/sql/relational-databases/tables/rename-tables-database-engine?view=sql-server-ver16
   
  - Rename Column
    
    link: https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-rename-transact-sql?redirectedfrom=MSDN&view=sql-server-ver16
    
    ```SQL
    USE [TS_Development3];
    
    GO
    EXEC sp_rename 'dbo.LU_UserStatus.StatusId', 'UserStatusId', 'COLUMN';
    GO
    ```
    
  - DROP TABLE (Transact-SQL)

    link: https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-table-transact-sql?view=sql-server-ver16

  - ADD a column in a table
    
    ```SQL
    ALTER TABLE <table_name>
    ADD <column_name> datatype;
    ```
  - Delete column in SQL
    
    ```SQL
    ALTER TABLE dbo.doc_exb DROP COLUMN <column_b;
    GO
    ```
    
- Create Tables

```SQL
CREATE TABLE AU_Role (
    RoleId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    Code VARCHAR(50),
    Name VARCHAR(100),
    IsActive BIT,
    RoleTypeId INT,
    Description VARCHAR(200)
);

CREATE TABLE AU_UserRole (
    UserRoleId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    RoleId INT,
    UserId INT,
    CreatedDate DATETIME,
    CreatedBy INT,
    EditedDate DATETIME,
    EditedBy INT,
    IsActive BIT,
    FOREIGN KEY (RoleId) REFERENCES AU_Role(RoleId)
);

```
