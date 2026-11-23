---
title: SQL Server Notes and Commands
description: A collection of tips, commands, and references for SQL Server, including backup scripts, SSMS customization, and common SQL operations.
type: content
path: development/databases/sqlserver.md
tags: [development, databases, sql-server, ssms, sql]
---
# SQL Server Notes and Commands

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## Parent Context

This document is part of the programming languages knowledge base, specifically for SQL and SQL Server.

## Contents Overview

This file provides a collection of tips, commands, and references for working with SQL Server, including backup scripts, UI customizations for SSMS, and common SQL operations for managing tables and columns.

## Role in System

This resource serves as a quick reference for developers and database administrators working with Microsoft SQL Server. It helps in performing routine tasks, troubleshooting, and understanding fundamental SQL operations within the SQL Server environment.

## Key Information and SQL Operations

### Backup Script

-   A visual reference for a database backup script.
    -   ![DB Backup Image](../images/sqlserver/backup-script.jpg)

### Dark Mode in SSMS (SQL Server Management Studio)

Instructions to enable dark mode:
1.  Navigate to `C:\Program Files (x86)\Microsoft SQL Server Management Studio 18\Common7\IDE`.
2.  Edit the file `ssms.pkgundef`. (Specific changes to the file are not detailed here but are implied).

### SQL Operations

#### Rename Tables

-   For more details, refer to the [Microsoft documentation on renaming tables](https://docs.microsoft.com/en-us/sql/relational-databases/tables/rename-tables-database-engine?view=sql-server-ver16).

#### Rename Column

```sql
EXEC sp_rename 'dbo.<table_name>.<old_column_name>', '<new_column_name>', 'COLUMN';
GO
```

#### DROP TABLE (Transact-SQL)

-   For more details, refer to the [Microsoft documentation on DROP TABLE](https://docs.microsoft.com/en-us/sql/t-sql/statements/drop-table-transact-sql?view=sql-server-ver16).

#### Add a Column to a Table

```sql
ALTER TABLE <table_name>
ADD <column_name> datatype;
```

#### Delete Column in SQL

```sql
ALTER TABLE dbo.doc_exb DROP COLUMN <column_b>;
GO
```
