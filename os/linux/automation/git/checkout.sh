#!/bin/bash

# Find all folders with git initialized (i.e., containing a .git folder)
git_dirs=$(find . -type d -name ".git" -exec dirname {} \;)

# If no git directories found, display a message and exit
if [ -z "$git_dirs" ]; then
    echo "No git repositories found in this directory or its subdirectories."
    exit 1
fi

# Loop through each Git directory and configure Git username and email
for dir in $git_dirs; do 
  (
    echo "Fetching all branches in git repository: $dir"
    cd "$dir" &&
      git fetch --all

    # Loop through all branches and check them out one by one
    for branch in $(git branch -r | grep -v '\->' | sed 's/origin\///'); do
      printf "\n\nCheckout on $branch\n\n"
      git checkout "$branch" || echo "Failed to checkout branch: $branch"
      git pull origin HEAD
    done

    # Check if the backup branch exists, if not create it
    backup_branch="backup/$dir_$(git config --get user.email)"

    if ! git rev-parse --verify "$backup_branch" >/dev/null 2>&1; then
      # Branch doesn't exist, so create it
      echo "Creating new backup branch: $backup_branch"
      git checkout -b "$backup_branch"
      # Uncomment the next line if you want to push the new branch
      # git push origin "$backup_branch"
    else
      # Branch exists, just pull the latest changes
      echo "Branch $backup_branch already exists. Pulling the latest changes."
      git checkout "$backup_branch" && git pull origin "$backup_branch"
    fi
  )

   printf "........................................................................\n\n"

done
