# **SQL**

### Backup Script

![DB Backup]('./images/backup-script.jpg')

- Dark mode SSMS

  navigate to `C:\Program Files (x86)\Microsoft SQL Server Management Studio 18\Common7\IDE`

  edit the file `ssms.pkgundef`

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
CREATE TABLE AU_User (
    UserId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
    FirstName VARCHAR(100),
	Surname	VARCHAR(100),
	DisplayName AS (FirstName + ' ' + Surname),
	EmailAddress VARCHAR(100),
	Password VARCHAR(MAX)	,
	PasswordUpdateDate DATETIME,
	AuthToken VARCHAR(MAX),
	LoginDate DATETIME,
	CreatedDate	DATETIME,
	CreatedBy INT,
	ModifiedDate DATETIME,
	ModifiedBy INT,
	IsActive BIT,
	ForgotPasswordGuid VARCHAR(MAX),
	ChangePasswordGuid VARCHAR(MAX),
	ShortCode AS (LEFT(FirstName, 1) + LEFT(Surname, 1)),
	ProfileUserImage VARCHAR(MAX),
	PhoneNumber VARCHAR(50),

	-- Indexes
	INDEX IX_UserId (UserId),
	INDEX IX_FirstName (FirstName),
	INDEX IX_Surname (Surname),
	INDEX IX_DisplayName (DisplayName),
	INDEX IX_EmailAddress (EmailAddress),
	INDEX IX_LoginDate (LoginDate),
	INDEX IX_CreatedDate (CreatedDate),
	INDEX IX_CreatedBy (CreatedBy),
	INDEX IX_ModifiedDate (ModifiedDate),
	INDEX IX_ModifiedBy (ModifiedBy),
)


CREATE TABLE AU_Role (
	RoleId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Code VARCHAR(50),
	Name VARCHAR(100),
	IsActive BIT,
	Description VARCHAR(200),
	CreatedBy INT,
	CreatedDate	DATETIME,
	ModifiedBy INT,
	ModifiedDate DATETIME,
	IsDeleted BIT

	-- Indexes
	INDEX IX_RoleId(RoleId),
	INDEX IX_Code (Code),
	INDEX IX_Name (Name),
)

CREATE TABLE AU_UserRole (
	UserRoleId INT IDENTITY(1,1) PRIMARY KEY NOT NULL,
	RoleId INT NOT NULL,
	UserId INT NOT NULL,
	CreatedDate DATETIME,
	CreatedBy INT,
	ModifiedDate DATETIME,
	ModifiedBy INT,
	IsActive BIT,

	-- Foreign key constraints
	FOREIGN KEY (RoleId) REFERENCES AU_Role(RoleId),
	FOREIGN KEY (UserId) REFERENCES AU_User(UserId),

	-- Indexes
	INDEX IX_UserRoleId (UserRoleId),
	INDEX IX_RoleId (RoleId),
	INDEX IX_UserId (UserId)
)

```
