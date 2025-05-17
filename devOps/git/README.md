# Git Update Script

A simple shell script to automate git workflow with safety checks and error handling.

## Usage

```bash
./git_update.sh "your commit message"
```

## What it does

1. Stashes any local changes
2. Pulls latest changes with rebase
3. Reapplies stashed changes
4. Adds all changes
5. Commits with provided message
6. Pushes to origin

## Requirements

- Git installed
- Repository initialized
- Remote origin configured

## Error Handling

- Validates commit message
- Handles pull conflicts
- Manages stashed changes
- Provides feedback for each step 