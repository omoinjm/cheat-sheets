# Create an EF Core Model from Database First (Scaffold DB Context)

We want to create a database context with code based models to represent this schema using a tool called `Scaffold DB Context`

## DotNet Cli

```bash
# check for the tools you have
dotnet tool list -g

# install the tool
dotnet tool install -g dotnet-ef
```

Create a database first model that we can use to access our database:

- Add packages to project:

```bash
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design
```

- Using the `dotnet-ef` tool

```bash
dotnet ef dbcontext scaffold `
"Server=localhost;Database=<dbName>;User=sa;Password=<Password>" `
Microsoft.EntityFrameworkCore.SqlServer `
--output-dir Models `
--context SomeThingDbContext `
--no-build
```

## Visual Studio

- Navigate to NuGet Package Manger

- Install `Microsoft.EntityFrameworkCore.Tools`

- Navigate to `Tools` -> `NuGet Package Manger` -> `Package Manager Console`

```powershell
Scaffold-DbContext -Connection "Server=localhost;Database=<dbName>;User=sa;Password=<Password>" -Provider Microsoft.EntityFrameworkCore.SqlServer -OutputDir Models -Context SomethingDbContext
```
