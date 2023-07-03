# ArchLinux on WSL2

## Method 

1. Install using docker

```bash
# pull the image
docker pull archlinux

# create container
 docker create -i archlinux bash

# start container
docker container start 188872160bba4

# interactive shell
docker exec -it 188872160bba4 /bin/bash
```

2. Setup a user

```bash
# setup pacman key
pacman-key --init

# add a user to the wheel group
useradd -m -G wheel omoi

# change password for that user
passwd omoi

# update the system
pacman -Syu

# install sudo and vim
pacman -Syu sudo vim

# we also want to make sure that the wheel group has sudo priviledges
vim /etc/sudoers
# or
EDITOR=vim visudo
# scroll down and uncomment
# %wheel ALL=(ALL:ALL) ALL
```

3. Export linux container into a path

```bash
# exit out of out docker container
exit

# export to tar file
docker export 188872160bb > /path/to/installation/archlinux.tar
# exit
```

4. Setup profile to login as create user

in windows terminal settings

```json
{
    "guid": "{a5a97cb8-8961-5535-816d-772efe0c6a3f}",
    "hidden": false,
    "icon": "D:\\omoi\\useful-stuff\\linux\\images\\icons\\arch.png",
    "name": "arch",
    "source": "Windows.Terminal.Wsl",
    "commandline": "wsl.exe -u omoi -d Arch"
}
```

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
