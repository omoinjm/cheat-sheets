# ArchLinux on WSL2

1. Basic installtion
  	- https://github.com/yuk7/ArchWSL
    - https://gist.github.com/ld100/3376435a4bb62ca0906b0cff9de4f94b#file-archlinuxwsl2-md
  
2. Package manager (yay)
    - https://github.com/Jguer/yay
    - https://www.tecmint.com/install-yay-aur-helper-in-arch-linux-and-manjaro/ 

3. How to set default user for manually installed WSL distro?
    - https://superuser.com/questions/1566022/how-to-set-default-user-for-manually-installed-wsl-distro
    - https://winaero.com/set-default-user-wsl-windows-10/

## Create new user

  -  edit the `/etc/wsl.conf` file to setup default user

```bash
[user]
default=username
```

```bash
sudo useradd exampleuser

# create the home directory for the user
sudo mkhomedir_helper exampleuser
```
 
5. Direnv Installation
    - https://direnv.net/docs/installation.html
  
6. Protocol Buffers and GRPC in Go 
    - https://dev.to/karankumarshreds/protocol-buffers-and-grpc-in-go-3eil

7. wsl2 docker start script
    - https://github.com/imjonos/wsl2-docker-start
