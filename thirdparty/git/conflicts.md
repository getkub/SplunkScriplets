- https://stackoverflow.com/questions/10697463/resolve-git-merge-conflicts-in-favor-of-their-changes-during-a-pull/33569970#33569970


## Resolve Git merge conflicts in favor of their changes
```
git pull -X theirs

OR 
git merge --strategy-option theirs


```

## If you're already in conflicted state, and you want to just accept all of theirs:
```
git checkout --theirs .
git add .
```


## Cherry pick
```
filename="path/to/the/conflicted_file.php"
hashid="1023e24"
git cherry-pick $hashid
git checkout --theirs $filename
git add $filename
```
