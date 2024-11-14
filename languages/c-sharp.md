# Create an EF Core Model from Database First (Scaffold DB Context)

[Install for Linux](https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu-2004)

In this guide, we will create a database context with code-based models to represent an existing database schema using the `Scaffold-DbContext` tool.

## DotNet CLI

### Check Installed Tools

To check which tools are already installed:

```bash
dotnet tool list -g

# Install the dotnet-ef tool globally:
dotnet tool install -g dotnet-ef
```

### Add Required Packages

Before scaffolding the database, you need to add the following packages to your project:

```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design
```

### Scaffold Database Context

Use the dotnet-ef tool to generate the model from the database. Replace `<dbName>` and `<Password>` with your actual database name and password:

```bash
dotnet ef dbcontext scaffold `
"Server=localhost;Database=<dbName>;User=sa;Password=<Password>" `
Microsoft.EntityFrameworkCore.SqlServer `
--output-dir Models `
--context SomeThingDbContext `
--no-build
```

## Visual Studio


### Install EF Core Tools

1. Open the NuGet Package Manager in Visual Studio.

2. Install the Microsoft.EntityFrameworkCore.Tools package.

### Scaffold Database Context Using Package Manager Console

1. Navigate to `Tools` -> `NuGet Package Manager` -> `Package Manager Console`.

2. Run the following command in the console, replacing `<dbName>` and `<Password>` with the actual values:

```powershell
Scaffold-DbContext -Connection "Server=localhost;Database=<dbName>;User=sa;Password=<Password>" -Provider Microsoft.EntityFrameworkCore.SqlServer -OutputDir Models -Context SomeThingDbContext
```
