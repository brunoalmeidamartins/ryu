#!/usr/bin/python2

from scapy.all import *

#dest = input("Destination: ")
#dest = raw_input("\nDestination: ")
#destport = input("Destination port: ") #Porta de destino

dest = '10.0.0.99'
destport = '1234'
ip = IP(dst=dest)
udp = UDP(dport=int(destport),sport=40000)
pkt = ip/udp
t = sr(pkt)
print(t)
