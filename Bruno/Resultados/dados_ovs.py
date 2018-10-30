#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Arquivo de plotagem de graficos - Versao 7.0

#import matplotlib.pyplot as plt
import commands
import time
import sys

i=0
tempo=205

#s3
rx1_aux = 0
rx2_aux = 0
#s1
tx1_aux = 0
tx2_aux = 0
tx3_aux = 0



lista = []
#lista2 = []
while i<tempo:
    #tx1=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F= '{print $2}' | awk -F, '{print $1}'"))
    ##tx1=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F= '{print $2}' | awk -F, '{print $1}'"))
    ##tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 2 | grep tx | awk -F= '{print $2}' | awk -F, '{print $1}'"))
    ##tx3=int(commands.getoutput("ovs-ofctl dump-ports s1 3 | grep tx | awk -F= '{print $2}' | awk -F, '{print $1}'"))

    #tx1=int(commands.getoutput("ovs-ofctl dump-ports r3 1 | grep rx | awk -F, '{print $2}' | awk -F= '{print $2}'")) #Switch s2 Port 1 "h4"
    #tx2=int(commands.getoutput("ovs-ofctl dump-ports r1 1 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'")) #Swtich s1 Port 1 "h1" Drop


    rx1=int(commands.getoutput("ovs-ofctl dump-ports s3 1 | grep rx | awk -F, '{print $2}' | awk -F= '{print $2}'"))
    rx2=int(commands.getoutput("ovs-ofctl dump-ports s3 2 | grep rx | awk -F, '{print $2}' | awk -F= '{print $2}'"))


    tx1=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))
    tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 2 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))
    tx3=int(commands.getoutput("ovs-ofctl dump-ports s1 3 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))



    #tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))
    #tx3=int(commands.getoutput("ovs-ofctl dump-ports s1 1 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))
    #tx2=int(commands.getoutput("ovs-ofctl dump-ports s1 2 | grep tx | awk -F, '{print $2}' | awk -F= '{print $2}'"))

    #x.append(i)
    #y1tx.append(tx1 - tx1_aux)
    if i >= 0 and i <=204:
        lista.append("r3->rx:"+str((tx1-tx1_aux))+" r1->tx:"+str((tx2 - tx2_aux))+'\n')
        #lista2.append("r3->tx:"+str((tx3-tx3_aux)*0.000001)+" r1->rx:"+str((tx4 - tx4_aux)*0.000001)+'\n')
        lista.append("s3->rx1:"+str(rx1-rx1_aux)+" s3->rx2:"+str(rx2-rx2_aux)+" s1->tx1:"+str(tx1-tx1_aux)+" s1->tx2:"+str(tx2-tx2_aux)+" s1->tx3:"+str(tx3-tx3_aux)+'\n')

    i+=1
    time.sleep(1)
    #print("r3->rx:"+str(tx1-tx1_aux)+" r1->tx:"+str(tx2 - tx2_aux))
    tx2_aux = tx2
    tx1_aux = tx1
    tx3_aux = tx3
    rx1_aux = rx1
    rx2_aux = rx2

    #tx3_aux = tx3
    #tx4_aux = tx4
arq = open('/home/bruno/ryu/Bruno/Resultados/Cenario1/SemIperf/teste'+sys.argv[1]+'.txt', 'w')
arq.writelines(lista)
arq.close()
'''
arq1 = open('/home/bruno/pox/ext/Dados/ComQoS/Com1Iperf/SaidaIperf/1/saida'+sys.argv[1]+'2.txt', 'w')
arq1.writelines(lista2)
arq1.close()
'''
