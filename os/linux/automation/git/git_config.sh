#!/bin/bash

# Check if enough arguments are passed
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <username> <email> [company]"
    exit 1
fi

# Get username and email from command line arguments
username=$1
email=$2

# If company is provided, use it; otherwise, extract from email
if [ -n "$3" ]; then
    company=$3
else
    company=$(echo "$email" | sed -E 's/^[^@]+@([^\.]+)\..*/\1/')
fi

# Validate the inputs
if [ -z "$username" ] || [ -z "$email" ] || [ -z "$company" ]; then
    echo "Inputs cannot be blank. Please provide username, email, and company (optional)."
    exit 1
fi

# Validate the username and company to ensure they are alphanumeric strings with a length of 1 to 25 characters
if ! echo "$username" | grep -qE '^[a-zA-Z0-9 ]{1,25}$' || ! echo "$company" | grep -qE '^[a-zA-Z0-9 ]{1,25}$'; then
    echo "Both username and company must be alphanumeric strings with a length of 1 to 25 characters."
    exit 1
fi

# Validate the email format
if ! echo "$email" | grep -qE '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'; then
    echo "Input must be a valid email address."
    exit 1
fi

# Find all folders with git initialized (i.e., containing a .git folder)
git_dirs=$(find . -type d -name ".git" -exec dirname {} \;)

# If no git directories found, display a message and exit
if [ -z "$git_dirs" ]; then
    echo "No git repositories found in this directory or its subdirectories."
    exit 1
fi

# Loop through each Git directory and configure Git username and email
for dir in $git_dirs; do
    echo "Configuring Git in repository: $dir"
    # Change directory to the git repository and set the username and email
    (
      cd "$dir" && 
        git config user.email "$email" &&
        git config user.name "$username" &&
        git config --local core.sshCommand "/usr/bin/ssh -i ~/.ssh/work/$company/id_rsa_$company"
    )

    printf "Git configuration done for $username <$email>\n"
    printf "...................................................\n\n"
done