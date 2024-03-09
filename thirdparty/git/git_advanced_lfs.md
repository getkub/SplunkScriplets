## Clone repo without pulling large files

https://stackoverflow.com/questions/42019529/how-to-clone-pull-a-git-repository-ignoring-lfs

```
brew install git-lfs
GIT_LFS_SKIP_SMUDGE=1 git clone SERVER-REPOSITORY

# Then specifically pull the relevant large file
lfname="some_large_file"
git-lfs pull --include ${lfname}
```