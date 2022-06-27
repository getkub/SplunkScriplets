# Measure Disk
- IOPS
- Bandwidth (BW)
- slat (Submission Latency)
- clat (Completion Latency)
- lat (Overall latency)

## Replicate Sequential write pattern
```
sudo apt -y install fio

```

## Edit configs
```
# vi /tmp/fio-seq-write.job

[global]
name=fio-seq-write
filename=fio-seq-write
rw=write
bs=16k
direct=1
numjobs=4
group_reporting
time_based
runtime=300

[file1]
size=10G
ioengine=libaio
iodepth=16
```

## Run FIO
```
sudo fio fio-seq-write.job
```
