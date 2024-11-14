# **SQL**

### Backup Script

![DB Backup](./images/sqlserver/backup-script.jpg)

### Dark Mode in SSMS

To enable dark mode in SQL Server Management Studio (SSMS):

1. Navigate to `C:\Program Files (x86)\Microsoft SQL Server Management Studio 18\Common7\IDE`.
2. Edit the file `ssms.pkgundef`.

### SQL Operations

#### Rename Tables (Database Engine)

For more information, refer to the [documentation on renaming tables](https://docs.microsoft.com/en-us/sql/relational-databases/tables/rename-tables-database-engine?view=sql-server-ver16).

#### Rename Column

To rename a column in a table:

```sql
EXEC sp_rename 'dbo.<table_name>.<old_column_name>', '<new_column_name>', 'COLUMN';
GO
```

### DROP TABLE (Transact-SQL)

To drop a table, see the [DROP TABLE documentation.](https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-table-transact-sql?view=sql-server-ver16).

### ADD a column in a table

```sql
ALTER TABLE <table_name>
ADD <column_name> datatype;
```

### Delete column in SQL

```sql
ALTER TABLE dbo.doc_exb DROP COLUMN <column_b>;
GO
```