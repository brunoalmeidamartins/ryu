#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Arquivo de plotagem de graficos - Versao 7.0

import matplotlib.pyplot as plt
import commands
import time

i=0
tempo=200
x=list()
y1tx=list()
y2tx=list()

plt.ion() #Turn interactive mode on
#fig,(ax1,ax2)=plt.subplots(2,sharex=True,sharey=True)
fig,ax1=plt.subplots(1,sharex=True,sharey=True)

fig.suptitle('Mbits/s - Roteador 1',fontsize=18)
#ax1.set_title('Interface eth1',fontsize=14)
#ax2.set_title('Interface eth2',fontsize=14)
plt.xlabel('Tempo(s)',fontsize=14)
ax1.set_ylabel('Largura de Banda(Mbits)',fontsize=14)
#ax2.set_ylabel('Mbits',fontsize=14)
ax1.grid()
#ax2.grid()
plt.axis([0,tempo,0,20])

tx1_ant=0
tx2_ant=0
while i<tempo:
    tx1=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx1_inst=(tx1-tx1_ant)/1048576
    tx1_inst=((tx1-tx1_ant)*8)/1048576
    tx1_ant=tx1

    tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 2 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx2_inst=(tx2-tx2_ant)/1048576
    tx2_inst=((tx2-tx2_ant)*8)/1048576
    tx2_ant=tx2

    x.append(i)
    y1tx.append(tx1_inst)
    y2tx.append(tx2_inst)

    ax1.plot(x,y1tx,'r-',label='TX eth1')
    ax1.plot(x,y2tx,'g-',label='TX eth2')

    if i==0:
        ax1.legend(loc='upper right',fontsize=12)
        #ax2.legend(loc='upper right',fontsize=12)

    plt.show()
    plt.pause(0.0001) #If there is an active figure it will be updated and displayed, and the GUI event loop will run during the pause
    i+=1
    time.sleep(1)
