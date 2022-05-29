## Rsync samples
```
### scp alternative
rsync -avz --remove-source-fiels -e ssh /this/dir remoteuser@remotehost:/remote/dir

### From remote systems
rsync -vtr --progress --exclude debug/ rsync://mirror.pnl.gov/epel/7/x86_64/ epel

### Faster rsync
rsync -r --size-only --progress ${srcDir}/* ${destDir}/ --dry-run
```
