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
