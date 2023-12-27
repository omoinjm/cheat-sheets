# Secure Linux Server

EVERYTHING IS HACKABLE, WE JUST WANT TO BE MORE SECURE

1. Enable Automatic Updates
2. Create a Limited User Account
3. Passwords are too weak
4. Lockdown Logins (harden ssh)
5. FIREWALLS

## Get a linux Server

Options:
  - Linode (100$ free credit for a year)
  - AWS Lightsail (first 3 months free, 3$ after that)

Connect to Lightsail instance via ssh:
  - https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-ssh-using-terminal
  
## STEP 1 - Enable Automatic Updates
  
Manual Updates:

```bash
apt update
apt dist-upgrade
```

Automatic Updates:

```bash
apt install unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades
```

![configure unattended-upgrades](./images/secure-linux-server/enable-updates.png)

Pick `<Yes>`

## STEP 2 - Create a Limited User Account

Create a user:

```bash
adduser <user>
```

Add user to the sudo group:

```bash
usermod -aG sudo <user>
```

## STEP 3 - Get rid of Password

Create the Public Key Directory on your Linux Server:

```bash
mdkir ~/.ssh && chmod 700 ~/.ssh
```

Create Public/Private keys on your computer:

```bash
ssh-keygen -b 4096
```
    
![ssh screenshot](./images/secure-linux-server/generate-ssh.png)

Upload your Public key to the your Linux Server (Windows):

```bash
scp $ENV:USERPROFILE/.ssh/id_rsa.pub {username}@{public-ip-address}:~/.ssh/authorized_keys
```

Upload your Public key to the your Linux Server (MAC):
```bash
scp ~/.ssh/id_rsa.pub {username}@{public-ip-address}:~/.ssh/authorized_keys
```

Upload your Public key to the your Linux Server (LINUX):

```bash
ssh-copy-id {username}@{public-ip-address}
```

## STEP 4 - Lockdown Logins
  
Edit the SSH config file:

```bash
sudo nano /etc/ssh/sshd_config
```

Allow private/public key pair login only

```txt
Port <pick different number>
AddressFamily inet

PermitRootLogin no

PasswordAuthentication no
```

Restart Service

```bash
sudo systemctl restart sshd
```

## STEP 5 - FIREWALL IT UP

See open ports

```bash
sudo ss -tupln
```

Install UFW

```bash
sudo apt install ufw
```

See UFW status

```bash
sudo ufw status
```

Allow port through firewall

```bash
sudo ufw allow {port number}
```

Enable Firewall

```bash
sudo ufw enable
```

Reload Firewall

```bash
sudo ufw reload
```

## Drop pings

Edit the UFW config file

```bash
sudo nano /etc/ufw/before.rules

# Add this line of config (at # ok icmp codes for INPUT):
-A ufw-before-input -p icmp --icmp-type echo-request -j DROP
```

Docs from [networkchuck](https://learn.networkchuck.com/courses/take/ad-free-youtube-videos/lessons/22626695-protect-your-linux-server-from-hackers-5-steps)