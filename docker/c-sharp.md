# Containerize a ASP .NET WEB API

## DockerFile

```dockerfile
# See https://aka.ms/customizecontainer to learn how to customize your debug container 
# and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443
# EXPOSE 5000

# Build Stage
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["./Grooove_Web_API.csproj", "./"]
RUN dotnet restore "./Grooove_Web_API.csproj"
COPY . .
WORKDIR /src
RUN dotnet build "./Grooove_Web_API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Grooove_Web_API.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Serve Stage
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Grooove_Web_API.dll"]
```

## Build the image

```bash
# Build the image from the docker file
docker build --rm -t grooovewebapi:dev .

# Show/view image
docker image ls

# Run the image
docker run --rm -p 5000:5000 -p 5001:5001 `
-e ASPNETCORE_HTTP_PORT=https://+:5001 `
-e ASPNETCORE_URLS=http://+:5000 `
omoi/grooovewebapi
```
