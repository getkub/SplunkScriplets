## Remove all history
```
git checkout main
git checkout --orphan newBranch
git add -A  # Add all files and commit them
git commit
git branch -D main  # Deletes the master branch
git branch -m main  # Rename the current branch to master
git push -f origin main  # Force push master branch to gitlab/github. Ensure it is UNPROTECTED
git gc --aggressive --prune=all     # remove the old files
```
