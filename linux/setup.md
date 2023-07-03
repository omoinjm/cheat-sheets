# ArchLinux on WSL2

## Method 1

## Method 2:

1. Basic installtion
  	- https://github.com/yuk7/ArchWSL
    - https://gist.github.com/ld100/3376435a4bb62ca0906b0cff9de4f94b#file-archlinuxwsl2-md
  
2. Package manager (yay)
    - https://github.com/Jguer/yay
    - https://www.tecmint.com/install-yay-aur-helper-in-arch-linux-and-manjaro/ 

```bash
# Update linux
sudo pacman -Sy

# Update your system's keyring by running the following command:
sudo pacman-key --init
sudo pacman-key --populate archlinux

# Clear the package cache to remove any corrupted files:
sudo pacman -Scc

sudo pacman -S binutils
```

3. How to set default user for manually installed WSL distro?
    - https://superuser.com/questions/1566022/how-to-set-default-user-for-manually-installed-wsl-distro
    - https://winaero.com/set-default-user-wsl-windows-10/
```bash
# Create new user
# edit the `/etc/wsl.conf` file to setup default user
[user]
default=username

# add user
sudo useradd exampleuser

# create the home directory for the user
sudo mkhomedir_helper exampleuser

# edit to add user to sudoers file
vim /etc/sudoers

omoi ALL=(ALL:ALL) ALL

# set up password
passwd omoi

# After the other "Defaults" line, add. This allow sudoers to use root password
Defaults rootpw
```
 
5. Direnv Installation
    - https://direnv.net/docs/installation.html
  
6. Protocol Buffers and GRPC in Go 
    - https://dev.to/karankumarshreds/protocol-buffers-and-grpc-in-go-3eil

7. wsl2 docker start script
    - https://github.com/imjonos/wsl2-docker-start
