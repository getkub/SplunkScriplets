#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a commit message"
    echo "Usage: ./git_update.sh 'your commit message'"
    exit 1
fi

# Store the commit message
COMMIT_MSG="$1"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Stashing local changes..."
    git stash
    STASHED=true
fi

# Pull with rebase
echo "Pulling latest changes..."
if ! git pull --rebase origin; then
    echo "Error: Failed to pull changes"
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
    exit 1
fi

# Reapply stashed changes if any
if [ "$STASHED" = true ]; then
    echo "Reapplying stashed changes..."
    git stash pop
fi

# Add all changes
echo "Adding changes..."
git add -A

# Commit
echo "Committing changes..."
git commit -m "$COMMIT_MSG"

# Push
echo "Pushing changes..."
if ! git push origin; then
    echo "Error: Failed to push changes"
    exit 1
fi

echo "Successfully updated repository!" 