
```
cd ~/somelocation/
launchctl load 145_scrolllock.plist
launchctl start 145_scrolllock

## Oneliner
mydir="~/Documents"
cd $mydir && launchctl load 145_scrolllock.plist && launchctl start 145_scrolllock && cd -
cd $mydir && launchctl stop 145_scrolllock && launchctl unload 145_scrolllock.plist && cd -
```

