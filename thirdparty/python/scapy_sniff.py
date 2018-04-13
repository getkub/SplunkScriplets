#!/usr/bin/env python2.7

# Script to use Scapy and Sniff out traffic based on filter. Similar to wireshark

from scapy.all import *

def pkt_callback(pkt):
   del pkt[Ether].src
   del pkt[Ether].dst
   del pkt[IP].chksum
   del pkt[UDP].chksum
   pkt[IP].dst = '192.168.100.100'
   sendp(pkt)
   pkt.show()

# sniff(iface='lo', filter='port 514', prn=lambda x: x.show(), store=0)
sniff(iface='lo', filter='port 514', prn=pkt_callback, store=0)

# filter have lot of options. eg 'udp port 514'
