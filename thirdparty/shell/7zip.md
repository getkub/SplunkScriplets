## Encrypt using 7zip
```
finalFile="myfilepackage.tgz"
pass="mypass"
src_file="src_file.txt"

7z a -p${pass} ${finalFile} ${src_file}
```
