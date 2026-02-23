# C# - EF Core Model from Database First

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../README.md)

## Parent Context

This document is part of the programming languages knowledge base, specifically for C# and Entity Framework Core.

## Contents Overview

This file provides a comprehensive guide on how to generate an Entity Framework Core model (database context and entity classes) from an existing database using a "database-first" approach. It covers instructions for both the .NET CLI and Visual Studio's Package Manager Console.

## Role in System

This documentation is crucial for C# developers working with existing SQL Server databases who need to quickly set up their application's data access layer using EF Core. It streamlines the process of scaffolding the database context and models, saving development time and ensuring consistency with the database schema.

## Key Steps and Commands

### .NET CLI

1.  **Install .NET SDK**: Ensure the .NET SDK is installed (linked for Linux installation).
2.  **Check/Install `dotnet-ef` Tool**: Verify or install the global `dotnet-ef` tool.
    ```bash
    dotnet tool list -g
    dotnet tool install -g dotnet-ef
    ```
3.  **Add Required NuGet Packages**: Add `Microsoft.EntityFrameworkCore.SqlServer` and `Microsoft.EntityFrameworkCore.Design` to your project.
    ```bash
    dotnet add package Microsoft.EntityFrameworkCore.SqlServer
    dotnet add package Microsoft.EntityFrameworkCore.Design
    ```
4.  **Scaffold Database Context**: Generate the model using the `dotnet ef dbcontext scaffold` command.
    ```bash
    dotnet ef dbcontext scaffold \
    "Server=localhost;Database=<dbName>;User=sa;Password=<Password>" \
    Microsoft.EntityFrameworkCore.SqlServer \
    --output-dir Models \
    --context SomeThingDbContext \
    --no-build
    ```

### Visual Studio

1.  **Install EF Core Tools**: Install the `Microsoft.EntityFrameworkCore.Tools` NuGet package.
2.  **Scaffold Database Context Using Package Manager Console**: Run the `Scaffold-DbContext` cmdlet in the Package Manager Console.
    ```powershell
    Scaffold-DbContext -Connection "Server=localhost;Database=<dbName>;User=sa;Password=<Password>" -Provider Microsoft.EntityFrameworkCore.SqlServer -OutputDir Models -Context SomeThingDbContext
    ```