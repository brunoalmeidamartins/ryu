#!/usr/bin/python2

from scapy.all import *

#dest = input("Destination: ")
dest = raw_input("\nDestination: ")
destport = input("Destination port: ") #Porta de destino

ip = IP(dst=dest)

udp = UDP(dport=int(destport))

raw = Raw(b'Olaa')

pkt = ip/udp/raw


t = sr(pkt)
#sr(pkt)
print(t)
