from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr
import sys
sr(IP(dst=sys.argv[1])/ICMP())
