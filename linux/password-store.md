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

4. Generate new passwords

```bash
pass generate <name>
```
