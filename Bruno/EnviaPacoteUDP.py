#!/usr/bin/python2

from scapy.all import *

#dest = input("Destination: ")
#dest = raw_input("\nDestination: ")
#destport = input("Destination port: ") #Porta de destino

dest = '10.0.0.99'

destport = '1234'

ip = IP(dst=dest)

udp = UDP(dport=int(destport),sport=40000)

raw = Raw(b'Quero um video 720p')

pkt = ip/udp/raw


t = sr(pkt)
#sr(pkt)
print(t)
