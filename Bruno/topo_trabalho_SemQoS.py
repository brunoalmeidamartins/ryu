#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from subprocess import call

import os
import time
import subprocess

path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

def myNetwork(i):

    net = Mininet( topo=None,
                   build=False,
                   host=CPULimitedHost,
                   link=TCLink,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6')
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7')
    srv1 = net.addHost('srv1', cls=Host, ip='10.0.0.8')
    srv2 = net.addHost('srv2', cls=Host, ip='10.0.0.9')

    info( '*** Add links\n')
    s1h1 = {'bw':25}
    net.addLink(s1, h1, cls=TCLink , **s1h1)
    s1h2 = {'bw':25}
    net.addLink(s1, h2, cls=TCLink , **s1h2)
    s1h3 = {'bw':25}
    net.addLink(s1, h3, cls=TCLink , **s1h3)
    s4h4 = {'bw':25}
    net.addLink(s4, h4, cls=TCLink , **s4h4)
    s4h5 = {'bw':25}
    net.addLink(s4, h5, cls=TCLink , **s4h5)
    s5h6 = {'bw':25}
    net.addLink(s5, h6, cls=TCLink , **s5h6)
    s5h7 = {'bw':25}
    net.addLink(s5, h7, cls=TCLink , **s5h7)
    s3h8 = {'bw':25}
    net.addLink(s3, h8, cls=TCLink , **s3h8)
    s3h9 = {'bw':25}
    net.addLink(s3, h9, cls=TCLink , **s3h9)
    s1s2 = {'bw':25}
    net.addLink(s1, s2, cls=TCLink , **s1s2)
    s3s2 = {'bw':25}
    net.addLink(s3, s2, cls=TCLink , **s3s2)
    s4s2 = {'bw':25}
    net.addLink(s4, s2, cls=TCLink , **s4s2)
    s5s2 = {'bw':25}
    net.addLink(s5, s2, cls=TCLink , **s5s2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s3').start([c0])
    net.get('s5').start([c0])
    net.get('s4').start([c0])
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    info( '*** Setting routes\n')
    h1.cmd('route add default dev h1-eth1')
    h2.cmd('route add default dev h2-eth1')
    h3.cmd('route add default dev h3-eth1')
    h4.cmd('route add default dev h4-eth1')
    h5.cmd('route add default dev h5-eth1')
    h6.cmd('route add default dev h6-eth1')
    h7.cmd('route add default dev h7-eth1')
    srv1.cmd('route add default dev srv1-eth1')
    srv2.cmd('route add default dev srv2-eth1')

    info( '*** Post configure switches and hosts\n')
    dumpNodeConnections(net.hosts)

    #Instala as filas de QoS
    os.system('python /home/bruno/ryu/Bruno/plotagem.py &')
    os.system('python /home/bruno/ryu/Bruno/admin.py &')
    os.system('python /home/bruno/ryu/Bruno/Resultados/dados_ovs.py '+str(i+1)+' 2 &') # 2 = 2 Iperf
    net.pingAll() #Pinga todos os hosts
    srv1.cmd('python /home/bruno/ryu/Bruno/EnviaPacoteUDP_Server.py &') #Envia pacote para instalar a regras de QoS
    h2.cmd('iperf -s -u &')
    h3.cmd('iperf -s -u &')

    print('Iperf 1 Iniciado!!!')
    srv2.cmd('iperf -c 10.0.0.2 -u -t 500 -i 1 -b 20m &')
    print('Iperf 2 Iniciado!!!')
    srv2.cmd('iperf -c 10.0.0.3 -u -t 500 -i 1 -b 20m &')
    time.sleep(29)
    print('Iniciando Server!!')
    srv1.cmd('python /home/bruno/ryu/Bruno/server_semQoS.py &')
    time.sleep(1)
    print('Iniciando Client!!')
    h1.cmd('python /home/bruno/ryu/Bruno/client_semQoS.py &')
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
    for i in range(0,30):
        myNetwork(i)
        time.sleep(30)
