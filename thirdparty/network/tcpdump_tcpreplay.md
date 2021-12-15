```
port=514
eth="ens0"
eth="any"
outfile="tcpdump.${port}.${eth}"
# capture packets
# tcpdump -s 0 port 514 -i eth0 -w /tmp/mycap.pcap 
tcpdump -vnn port $port -i $eth -w /tmp/${outfile}.pcap
# or try below
tcpdump -i any port $port -vnn -w /tmp/${outfile}.pcap
# For further filtering (use and/or operators)
tcpdump -i any src 10.20.30.40 and port 514 -vnn
```

### To print in plaintext
```
#tcpdump -XX -r /tmp/mycap.pcap > /tmp/mycap.txt
#tshark -x -r /tmp/mycap.pcap > /tmp/mycap.txt
tcpdump -XX -r /tmp/${outfile}.pcap > /tmp/${outfile}.txt
```

###  Now tcprewrite the file with correct source/mac etc
```
tcprewrite --enet-vlan=del --infile=/tmp/${outfile}.pcap --outfile=/tmp/rewrite.${outfile}.pcap
```

### tcpreplay commands
### CAn accept only UDP or ICMP  (NOT TCP)
```
tcpreplay --intf1=$eth  /tmp/rewrite.${outfile}.pcap
```

### To grep directly
```
tcpdump -nnAs0 -i any port $port | grep -i my_keyword  
```

### Other formats and advanced Examples
```
# https://danielmiessler.com/study/tcpdump/
tcpdump -ttnnvvS  # RAW output
tcpdump -nvX src net 192.168.0.0/16 and dst net 10.0.0.0/8 or 172.16.0.0/16
tcpdump dst 192.168.0.2 and src net and not icmp
tcpdump -vvAls0 | grep 'User-Agent:'

# group your options using single quotes
tcpdump 'src 10.0.2.4 and (dst port 3389 or 22)'
#isolate tcp flags
tcpdump 'tcp[tcpflags] == tcp-rst'
tcpdump 'tcp[13] & 2!=0'
tcpdump 'tcp[tcpflags] == tcp-syn'
tcpdump 'tcp[tcpflags] == tcp-ack'

# SSH connections
tcpdump 'tcp[(tcp[12]>>2):4] = 0x5353482D'

```
