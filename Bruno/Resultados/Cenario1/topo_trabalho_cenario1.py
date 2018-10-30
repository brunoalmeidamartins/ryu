#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

import os
import time
import subprocess

def myNetwork(i):

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    srv1 = net.addHost('srv1', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    srv2 = net.addHost('srv2', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)

    info( '*** Add links\n')

    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s3, srv1)
    net.addLink(s3, srv2)
    net.addLink(s4, h4)
    net.addLink(s4, h5)
    net.addLink(s5, h6)
    net.addLink(s5, h7)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s2, s4)
    net.addLink(s2, s5)



    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s5').start([c0])
    net.get('s2').start([c0])
    net.get('s1').start([c0])
    net.get('s4').start([c0])
    net.get('s3').start([c0])

    info( '*** Post configure switches and hosts\n')
    #Comandos a serem executados
    os.system('python /home/bruno/ryu/Bruno/Resultados/dados_ovs.py '+str(i+1)+' &')
    os.system('python /home/bruno/ryu/Bruno/admin.py &')
    h2.cmd('iperf -s -u &')
    h3.cmd('iperf -s -u &')
    srv2.cmd('iperf -c 10.0.0.2 -u -t 205 -i 1 -b 19m &')
    srv2.cmd('iperf -c 10.0.0.3 -u -t 205 -i 1 -b 19m &')
    time.sleep(29)
    srv1.cmd('python /home/bruno/ryu/Bruno/server.py &')
    time.sleep(1)
    h1.cmd('python /home/bruno/ryu/Bruno/client.py &')
    time.sleep(1)
    print('Rodada: '+str(i+1))
    for r in range(32,215):
        if r%10 == 0:
            print('Tempo: '+str(r)+' Rodada: '+str(i+1))
        time.sleep(1)

    #CLI(net)
    info('*** Fim...Aguardando os 30 segundos!!!')
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    for i in range(0,1):
        myNetwork(i)
        time.sleep(30)
