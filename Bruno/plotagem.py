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
y3tx=list()

y1rx=list()
y2rx=list()

plt.ion() #Turn interactive mode on
#fig,(ax1,ax2)=plt.subplots(2,sharex=True,sharey=True)
fig,ax1=plt.subplots(1,sharex=True,sharey=True)

fig.suptitle('Mbits/s - Dados',fontsize=18)
#ax1.set_title('Interface eth1',fontsize=14)
#ax2.set_title('Interface eth2',fontsize=14)
plt.xlabel('Tempo(s)',fontsize=14)
ax1.set_ylabel('Largura de Banda(Mbits)',fontsize=14)
#ax2.set_ylabel('Mbits',fontsize=14)
ax1.grid()
#ax2.grid()
plt.axis([0,tempo,0,25])

tx1_ant=0
tx2_ant=0
tx3_ant=0

rx1_ant=0
rx2_ant=0
while i<tempo:
    tx1=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx1_inst=(tx1-tx1_ant)/1048576
    tx1_inst=((tx1-tx1_ant)*8)/1048576
    tx1_ant=tx1

    tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 2 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx2_inst=(tx2-tx2_ant)/1048576
    tx2_inst=((tx2-tx2_ant)*8)/1048576
    tx2_ant=tx2

    tx3=int(commands.getoutput("ovs-ofctl dump-ports s1 3 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx2_inst=(tx2-tx2_ant)/1048576
    tx3_inst=((tx3-tx3_ant)*8)/1048576
    tx3_ant=tx3

    rx1=int(commands.getoutput("ovs-ofctl dump-ports s3 1 | grep rx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx1_inst=(tx1-tx1_ant)/1048576
    rx1_inst=((rx1-rx1_ant)*8)/1048576
    rx1_ant=rx1

    rx2=int(commands.getoutput("ovs-ofctl dump-ports s3 2 | grep tx | awk -F, '{print $2}' | awk -F, '{print $1}' | awk -F= '{print $2}'"))
    #tx1_inst=(tx1-tx1_ant)/1048576
    rx2_inst=((rx2-rx2_ant)*8)/1048576
    rx2_ant=rx2



    x.append(i)
    y1tx.append(tx1_inst)
    y2tx.append(tx2_inst)
    y3tx.append(tx3_inst)

    y1rx.append(rx1_inst)
    y2rx.append(rx2_inst)

    ax1.plot(x,y1tx,'r-',label='TXs1 eth1')
    ax1.plot(x,y2tx,'g-',label='TXs1 eth2')
    ax1.plot(x,y3tx,'b-',label='TXs1 eth3')

    ax1.plot(x,y1rx,'y-',label='RXs3 eth1')
    #ax1.plot(x,y2rx,'p-',label='RXs3 eth2')

    if i==0:
        ax1.legend(loc='upper right',fontsize=12)
        #ax2.legend(loc='upper right',fontsize=12)

    plt.show()
    plt.pause(0.0001) #If there is an active figure it will be updated and displayed, and the GUI event loop will run during the pause
    i+=1
    time.sleep(1)
