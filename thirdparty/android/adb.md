## MacOS

```
brew install android-platform-tools
```

## Push & Pull (copy)
```
src="~/Documents/data/music.mp3"
dest="/storage/self/primary/Audiobooks/"
adb push $src $dest
```

## Delete
```
fileName="/storage/self/primary/Audiobooks/AB*.mp3"
adb shell rm $fileName
```
