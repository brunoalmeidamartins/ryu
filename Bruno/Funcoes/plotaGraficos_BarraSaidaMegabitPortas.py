#import matplotlib.pyplot as plt
from pylab import *
#from media_arquivo_bytes_fun import obtemDadosLeitura
#from media_iperf import obtemVetorIperf
#from MontaVetores import RetornaVetoresArquivos as vetores
#from MontaVetores import RetornaVetoresComMedias as vetoresMedia
from MontaVetores import RetornaMediaSaidaPortasBytesPortas as MediaPortasBytes
t = 6
#for i in range (0,3):
cenario = '3'
for j in range (0,3):
    #cenario = str(j+1) #Cenario = [1,2,3]
    teste = j #Teste = [0,1,2]
    #print('Cenario: '+cenario+', Teste: '+teste)


    s1_tx1,s1_tx2,s1_tx3,s3_rx1,s3_rx2 = MediaPortasBytes(cenario,str(teste))
    '''
    #Convertendo em Megabits
    s1_tx1 = s1_tx1*0.000008
    s1_tx2 = s1_tx2*0.000008
    s1_tx3 = s1_tx3*0.000008
    s3_rx1 = s3_rx1*0.000008
    s3_rx2 = s3_rx2*0.000008
    '''
    '''
    #Convertendo em Megabyte
    s1_tx1 = s1_tx1*0.000001
    s1_tx2 = s1_tx2*0.000001
    s1_tx3 = s1_tx3*0.000001
    s3_rx1 = s3_rx1*0.000001
    s3_rx2 = s3_rx2*0.000001
    '''

    '''
    pos = arange(5) + .5

    #barh(pos,(s3_rx1,s1_tx1,s3_rx2,s1_tx2,s1_tx3),align='center',color='#b8ff5c')
    barh(pos,(s1_tx3,s1_tx2,s3_rx2,s1_tx1,s3_rx1),align='center',color='red') #Saida_Iperf2, Saida_Iperf1, Entrada_Iperf, Saida_Video, Entrada_Video
    yticks(pos,('Saída_Iperf_2','Saída_Iperf_1','Entrada_Iperf','Saída_Vídeo','Entrada_Vídeo'))
    '''
    if teste == 0:
        print("Teste: "+str(teste))
        pos = arange(2) + .5
        barh(pos,(s1_tx1,s3_rx1),align='center',color='red') #Saida_Video, Entrada_Video
        yticks(pos,('S_Vídeo','E_Vídeo'))
        title('Gráfico das saídas produzidas sem carga de trabalho')
        xlabel('Total de Bytes(B) gerados')
        #ylabel('Medições')
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_SemIperf.png',dpi=720)
    elif teste == 1:
        print("Teste: "+str(teste))
        pos = arange(4) + .5
        barh(pos,(s1_tx2,s3_rx2,s1_tx1,s3_rx1),align='center',color='red') #Saida_Iperf1, Entrada_Iperf, Saida_Video, Entrada_Video
        yticks(pos,('S_Iperf_1','E_Iperf','S_Vídeo','E_Vídeo'))
        title('Gráfico das saídas produzidas com uma carga de trabalho')
        xlabel('Total de Bytes(B) gerados')
        #ylabel('Medições')
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_1Iperf.png',dpi=720)
    else:
        print("Teste: "+str(teste))
        pos = arange(5) + .5
        barh(pos,(s1_tx3,s1_tx2,s3_rx2,s1_tx1,s3_rx1),align='center',color='red') #Saida_Iperf2, Saida_Iperf1, Entrada_Iperf, Saida_Video, Entrada_Video
        yticks(pos,('S_Iperf_2','S_Iperf_1','E_Iperf','S_Vídeo','E_Vídeo'))
        title('Gráfico das saídas produzidas com duas cargas de trabalho')
        xlabel('Total de Bytes(B) gerados')
        #ylabel('Medições')
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_2Iperf.png',dpi=720)
    '''
    #grid(True)
    if teste == 0:
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_SemIperf.png',dpi=720)
    elif teste == 1:
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_1Iperf.png',dpi=720)
    else:
        savefig('/home/bruno/ryu/Bruno/Resultados/Graficos/Barra/0'+str(t+1)+'_Cenario'+cenario+'_2Iperf.png',dpi=720)
    #show()
    '''
    t = t + 1
