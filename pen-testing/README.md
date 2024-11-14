# Pentesting Repositories

## Hakrawler
  
- **Description**: A fast Golang web crawler designed to gather URLs and JavaScript file locations. It is a simple implementation of the powerful Gocolly library.

- **Link**: [Hakrawler GitHub Repository](https://github.com/hakluke/hakrawler)

## Notes

### Nmap Scan

- Run the following command to perform a SYN scan and version detection:

```bash
sudo nmap -sS -sV <ip address>
```

### Connecting to different protocols/services

Telnet
 
- Port: 22/tcp
- Command:

```bash 
telnet <ip address>
```
    
FTP 

- Port: 21/tcp 
- Command:
    
```bash
ftp <ip address>
```
    
SMB

- Port: 445/tcp
- Command:

```bash
smbclient //ip address/Sharename
```
