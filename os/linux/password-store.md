# Terminal Password Manager

1. Generate key pair

```bash
# prompted by identity information and master password
gpg --gen-key

# list ID of generated key
gpg -K

# N/B: newly created keys have an expiration date
# change it using
gpg --edit-key <key-id>

# then call
expire

# and set to 0
# "0 = key does not expire"

# when done type
save

```

2. Initialize a new password store

```bash
pass init <key-id>
```

3. Turn the password store into a git repository

```bash
pass init git
```

4. Insert and a into a head
```bash
# This way of setting a password is not very strong
pass insert github
```

5. Generate new passwords

```bash
pass generate <name>
```

## Organisation

1. We can organise our passwords like we would in a file system

```bash
# pass will create a directory in our store called 'github'
# which will then contain a file of our encrypted password called 'personal'
pass generate github/personal
```

2. We can nest directories as well

```bash
pass generate aws/personal/account
```

3. Organising our directories this way makes it easier to use the `find` command.

```bash
# This will show you all of the passwords you have in your store.
pass
```

```bash
pass find github
```

## Store email with the password 

Pass allows you to add extra information as metadata (this will be encrypted as well).

1. We can edit a password file

```bash
pass edit github/personal
```

```txt
# Password
qweerrtrthty

# Add extra data under the password
email: example@gmail.com
```

## Forgot which file you stored your password in?

1. Search for the email you stored in under

```bash
pass grep "example@gmail.com"

# You can also grep the email metadata as well
pass grep "email:"
```

## Get passwords out of `password-store`

1. Show command in `stdout`

```bash
pass show github/personal

# A better way is to copy it into our clipboard
pass show -c github/persoanl

# show contents of clipboard
xclip -o -sel clip
```

## Remove passwords

```bash
pass rm github/personal
```

1. Revert the change if deleted by mistake

```bash
# Show commit history
pass git log

# Look for which commit you want to revert to and revert back to it
pass git revert HEAD
```

## Set up a remote repository

This will serve as a backup and it will be easily downloaded onto other devices

1. Add a remote to repo

```bash
pass git remote add origin git@github.com:<user>/<repo>

pass git push origin main
```

2. Load onto another machine

```bash
# Make sure to install pass on the other machine
pass git clone git@github.com:<user>/<repo> .password-store
```

3. Machaine won't have private key to decrypt the passwords

```bash
# Go back to machine with the original password-store and export the keys

mkdir exported-keys
cd exported-keys

# Export public key
# Exports the public.pgp to a base64 file
gpg --output public.pgp --armor --export example@gmail.com

# Export private key
# You'll be prompted for a password
gpg --output private.pgp --armor --export-secret-key example@gmail.com
```

4. Transfer the keys using your preferred method (SSH in this case)

```bash
scp -r <user>@<serverip>:exported-keys .
```

5. Import the keys

```bash
# You'll be prompted for a password
gpg --import private.pgp

gpg --import public.pgp
```

## Add more permissions (trust level) to public key on new machine in order to encrypt new passwords

```bash
gpg --edit-key njmcloud@gmail.com

# Once inside gpg call the trust command
gpg> trust
# Assign maxium trust value for the machine
5
save
```

## Integrate into work flow

Environment variables

1. This prevents accidentally pasting secret keys into your terminal session which can be dangerous as it can stay in your shell history file for a long time

```bash
# For linux
export GITHUB_TOKEN=$(pass show github/api/token)
```

2. Secure any cli commands that require an api token

```bash
aws lambda list-functions --region=us-east-1
# Response: Unable to locate credentials. You can configure credentials by running "aws configure"

# You can use an alias as part of that command to create access credentials
alias aws="AWS_ACCESS_KEY_ID=$(pass show aws/access_id) AWS_SECRETS_ACCESS_KEY=$(pass show aws/access_token) aws"

# This will authenticate the tool automatically
aws lambda list-functions --region=us-east-1
# Response: { "Functions": [] }
```


