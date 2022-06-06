```
lsblk -io KNAME,TYPE,SIZE,MODEL,LABEL
```

## Will show Start/End and Blocks
```
fdisk -l  /dev/sda   
# https://support.microsoft.com/en-us/kb/929491
```

## Bad sectors in Hard Disk
```
sudo hdparm -Ttv /dev/sda
```

## dd commands and showing disk write speed
```
dd if=/dev/zero of=/pv-1tb-0/dd.test bs=32k count=100000 oflag=direct
```
