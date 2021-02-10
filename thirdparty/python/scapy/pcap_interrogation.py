from scapy.all import *
from scapy.utils import rdpcap

conf.L3socket
conf.L3socket=L3RawSocket

pkts=rdpcap("/tmp/sample.pcap",10)  # could be used like this rdpcap("filename",500) fetches first 500 pkts
for pkt in pkts:
    #print 'IP_src=' + pkt[IP].src + ' IP_dst=' + pkt[IP].dst + ' sport=' + str(pkt[UDP].sport) + ' dport=' + str(pkt[UDP].dport)
    print pkt[IP].show()
    #  sendp(pkt) #sending packet at layer 2
