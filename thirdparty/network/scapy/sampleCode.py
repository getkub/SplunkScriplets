import sys
sys.path.insert(0, '/configs/scapy')
from scapy.all import *

conf.L3socket
conf.L3socket=L3RawSocket
packet = IP(dst="127.0.0.1", src="10.121.122.122")/UDP(sport=333, dport=514)/Raw(load='<165>1 2018-06-29T10:14:15.003Z machine.test mylog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"] MY_AN_MSG application event log entry')

send(packet)
