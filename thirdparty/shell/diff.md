### side by side
```
diff -y file1 file2
```

### Width adjustment of side by side
```
diff -W $(( $(tput cols) -2 )) -y file1 file2
```
