## Soak Test Network - iPerf
```
sudo apt -y install iperf3
iperf3 -s

iperf3 -c server2 -p 8000 -t 300
```
