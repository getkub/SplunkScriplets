If the Branch have conflicts, but needs to ensure Branch overpower the master

https://stackoverflow.com/questions/2862590/how-to-replace-master-branch-in-git-entirely-from-another-branch

```
mybranch="my_branch"
git checkout $mybranch
git merge -s ours master
git checkout master
git merge $mybranch
```
