
```
filename="/my/path/file"
```

## Follow file
```
git log --follow $filename 
git log --oneline --follow $filename 
```

## diff the same file between two different commits
```
git diff HEAD~2 HEAD -- $filename
git diff c598d3fe a0647d42 -- $filename
```

## Git: checkout a single file from a specific commit
```
git checkout c598d3fe $filename
```
