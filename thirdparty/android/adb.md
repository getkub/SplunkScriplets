## MacOS

```
brew install android-platform-tools
```

## List/View
```
fName="/storage/self/primary/Audiobooks/AB*.mp3"
adb shell ls -l $fName
```

## Push & Pull (copy)
```
src="~/Documents/data/music.mp3"
dest="/storage/self/primary/Audiobooks/"
adb push $src $dest
```

## Delete
```
fName="/storage/self/primary/Audiobooks/AB*.mp3"
adb shell rm $fName
```
