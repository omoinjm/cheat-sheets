# Docker

## OSINT Phone Number

- **Links**: [PhoneInfoga Getting Started Guide](https://sundowndev.github.io/phoneinfoga/getting-started/install/)

- **Download**: 

```bash
docker pull sundowndev/phoneinfoga:latest
```

- **Check Version**: 

```bash
docker run --rm -it sundowndev/phoneinfoga version
```

- **Run Scan in Terminal**: 

```bash
docker run --rm -it sundowndev/phoneinfoga scan -n <number>
```  

- **Access Web UI**:

```bash
docker run --rm -it -p 8080:8080 sundowndev/phoneinfoga serve -p 8080
```