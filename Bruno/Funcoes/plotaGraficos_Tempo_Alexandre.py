import matplotlib.pyplot as plt
from MontaVetores import RetornaVetoresComMedias as vetoresMedia

#RetornaVetoresComMedias('3','2')


x = [] #tempo
y1 = [] # s1-TX-Port1
y2 = [] # s1-TX-Port2
y3 = [] # s1-TX-Port3
y4 = [] #s3-RX-Port1
y5 = [] #s3-RX-Port2
#y3 = [] #media da saida rx R3

#y4 = [] #Saida 1 do iperf
#y5 = [] #Saida 2 do Iperf
#y6 = [] #Saida 3 do Iperf
#y7 = [] #Saida 4 do Iperf


cenario = '3'
teste = '2'
#y1,y2,y3,y4,y5 = vetores('1','1','15') #Teste, Cenario, num_arq Onde Teste=0,1,2=Iperf,  Cenario=1,2,3, num_arq=[1,...,30]
y1,y2,y3,y4,y5 = vetoresMedia(cenario,teste) #Cenario,Tese    Onde Cenario=1,2,3 Teste=0,1,2=Iperf,





for i in range(0,len(y1)): #TempoCerto
    x.append(i)
    #y1.append(int((dados[i][0])*1**(-6)))
    #y2.append(int((dados[i][1])*1**(-6
    y1[i] = y1[i]*0.000008
    y2[i] = y2[i]*0.000008
    y3[i] = y3[i]*0.000008
    #y1.append(int(dados[i][0]*0.000008))
    #y2.append(int(dados[i][1]*0.000008))
    #y3.append(int(dados[i][1]*0.000008))
#print(len(y1))
'''
somatorio = 0
for i in y1:
    somatorio = somatorio + i
media = int(somatorio/len(y1))
#print(media)
for i in range(0,len(y1)):
    y3.append(media)
#print(y3) #Media da saida do VLC

#vet_temp1 = obtemVetorIperf(path2) #Vetor Iperf
#vet_temp2 = obtemVetorIperf(path3) #Vetor Iperf
#vet_temp3 = obtemVetorIperf(path4) #Vetor Iperf
#vet_temp4 = obtemVetorIperf(path5) #Vetor Iperf

#print(len(vet_temp1)
'''
'''
Reduzindo os vetores para tam 112
'''
'''
aux1 = []
aux2 = []
aux3 = []
aux4 = []
for i in range(0,112):
    aux1.append(x[i])
    aux2.append(y1[i])
    aux3.append(y2[i])
    aux4.append(y3[i])
x = aux1
y1 = aux2
y2 = aux3
y3 = aux4
'''
'''
Fim da reducao
'''

#for i in range(0,112): #Copia o vetor de iperf ate o tamanho de y1 e y2
    #y4.append(int(vet_temp1[i])*125000) #Converte Mbits em Bytes
    #y5.append(int(vet_temp2[i])*125000) #Converte Mbits em Bytes
    #y6.append(int(vet_temp3[i])*125000) #Converte Mbits em Bytes
    #y7.append(int(vet_temp4[i])*125000) #Converte Mbits em Bytes

#print(y4)
#print(y1)


fig,ax1 = plt.subplots()
if teste == '0':
    ax1.plot(x,y1,'r-',linewidth=1.5,linestyle='-', label=u'Video Out')
elif teste == '1':
    ax1.plot(x,y1,'r-',linewidth=1.5,linestyle='-', label=u'Video Out')
    ax1.plot(x,y2,'g-',linewidth=1.5,linestyle='-',label=u'iPerf 1 Out' )
else:
    ax1.plot(x,y1,'r-',linewidth=1.5,linestyle='-', label=u'Video Out')
    ax1.plot(x,y2,'g-',linewidth=1.5,linestyle='-',label=u'iPerf 1 Out' )
    ax1.plot(x,y3,'y-',linewidth=1.5,linestyle='-',label=u'iPerf 2 Out')
#ax1.plot(x,y4,'b',linewidth=1.5,linestyle='-',label='Iperf 1')
#ax1.plot(x,y5,'g',linewidth=1.5,linestyle='-',label='Iperf 2')
#ax1.plot(x,y6,'y',linewidth=1.5,linestyle='-',label='Iperf 3')
#Propriedade do Graficos
#ax1([0,len(x),0,1000])
#Limites do grafico
ax1.set_ylim(0,25)
ax1.set_xlim(0,180) #O tempo correto eh 205






'''
ax2 = fig.add_subplot(1,2,2)
ax2.plot(x,y4,'b',linewidth=1.5,linestyle='-',label='Iperf 1')
#ax2.plot(x,y5,'g',linewidth=1.5,linestyle='-',label='Iperf 2')
#ax2.plot(x,y6,'y',linewidth=1.5,linestyle='-',label='Iperf 3')
#ax2.plot(x,y7,'r',linewidth=1.5,linestyle='-',label='Iperf 4')
#Limites do Grafico
ax2.set_ylim(1600000000,2200000000)
ax2.set_xlim(0,112)
'''


##Propriedades do Grafico
#ax1.tick_params(axis='x',colors='c')
#ax1.tick_params(axis='y',colors='c')
#ax2.tick_params(axis='x',colors='c')
#ax2.tick_params(axis='y',colors='c')

#ax1.yaxis.label.set_color('c')
#ax1.xaxis.label.set_color('c')
#ax2.yaxis.label.set_color('c')
#ax2.xaxis.label.set_color('c')



ax1.legend(loc='upper right') #Local das legendas
#ax2.legend(loc='upper right') #Local das Legendas

#ax1.yaxis.label.set_color('c')
#ax1.xaxis.label.set_color('c')

ax1.set_xlabel('Time(s)',fontsize=14)
ax1.set_ylabel('Megabits',fontsize=16)
#ax2.set_title('Grafico Iperf')
#ax2.set_xlabel('tempo(s)')
#ax2.set_ylabel('Bytes')

plt.show()

'''
if teste == '0':
    plt.savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Cenario'+cenario+'_SemIperf.png')
elif teste == '1':
    plt.savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Cenario'+cenario+'_1Iperf.png')
else:
    plt.savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Cenario'+cenario+'_2Iperf.png')
'''