import os
path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

def RetornaVetoresArquivos(tes,cen,num_arq): #teste,cenario,num_arquivo
    teste = tes # 0 = Sem Iperf, 1 = 1Iperf, 2 = 2Iperf
    pasta = ''
    cenario = cen #1 , 2 ou 3
    s1_tx1 = [] #Porta 1 do Switch 1
    s1_tx2 = [] #Porta 2 do Switch 1
    s1_tx3 = [] #Porta 3 do Switch 1
    s3_rx1 = [] #Porta 1 do Switch 3
    s3_rx2 = [] #Porta 2 do Switch 3
    if teste == '0':
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/SemIperf/'
        #print('Sem Iperf')
    elif teste == '1':
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/1Iperf/'
        #print('1 Iperf')
    else:
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/2Iperf/'
        #print('2 Iperf')
    #for j in range (0,30):
    arq = open(pasta+'teste'+num_arq+'.txt', 'r')
    #print('Path Arq: '+pasta+'teste'+num_arq+'.txt')
    texto = arq.readlines()
    for i in texto:
        vet = i.split(' ')
        vet[0] = vet[0].replace('s3->rx1:','')
        vet[1] = vet[1].replace('s3->rx2:','')
        vet[2] = vet[2].replace('s1->tx1:','')
        vet[3] = vet[3].replace('s1->tx2:','')
        vet[4] = vet[4].replace('s1->tx3:','')
        vet[4] = vet[4].replace('\n','')
        s1_tx1.append(float(vet[2]))
        s1_tx2.append(float(vet[3]))
        s1_tx3.append(float(vet[4]))
        s3_rx1.append(float(vet[0]))
        s3_rx2.append(float(vet[1]))

    arq.close()
    return s1_tx1,s1_tx2,s1_tx3,s3_rx1,s3_rx2

def RetornaVetoresComMedias(cen, tes): #Recebe o cenario e o Teste; Devolve a media dos 30 arquivos
    vet_s1_tx1 = []
    vet_s1_tx2 = []
    vet_s1_tx3 = []
    vet_s3_rx1 = []
    vet_s3_rx2 = []

    vet_aux_tx1 = []
    vet_aux_tx2 = []
    vet_aux_tx3 = []
    vet_aux_rx1 = []
    vet_aux_rx2 = []
    for i in range(0,30):
        vet_aux_tx1,vet_aux_tx2,vet_aux_tx3,vet_aux_rx1,vet_aux_rx2 = RetornaVetoresArquivos(tes,cen,str(i+1))
        vet_s1_tx1.append(vet_aux_tx1)
        vet_s1_tx2.append(vet_aux_tx2)
        vet_s1_tx3.append(vet_aux_tx3)
        vet_s3_rx1.append(vet_aux_rx1)
        vet_s3_rx2.append(vet_aux_rx2)

    vet_aux_tx1 = []
    vet_aux_tx2 = []
    vet_aux_tx3 = []
    vet_aux_rx1 = []
    vet_aux_rx2 = []

    for i in range(0,205):
        #print(len(vet_s1_tx1[i]))
        somatorio_tx1 = 0
        somatorio_tx2 = 0
        somatorio_tx3 = 0
        somatorio_rx1 = 0
        somatorio_rx2 = 0
        for j in range(0,30):
            somatorio_tx1 = somatorio_tx1 + vet_s1_tx1[j][i]
            somatorio_tx2 = somatorio_tx2 + vet_s1_tx2[j][i]
            somatorio_tx3 = somatorio_tx3 + vet_s1_tx3[j][i]
            somatorio_rx1 = somatorio_rx1 + vet_s3_rx1[j][i]
            somatorio_rx2 = somatorio_rx2 + vet_s3_rx2[j][i]
        vet_aux_tx1.append(somatorio_tx1/30)
        vet_aux_tx2.append(somatorio_tx2/30)
        vet_aux_tx3.append(somatorio_tx3/30)
        vet_aux_rx1.append(somatorio_rx1/30)
        vet_aux_rx2.append(somatorio_rx2/30)
    return vet_aux_tx1,vet_aux_tx2,vet_aux_tx3,vet_aux_rx1,vet_aux_rx1
def RetornaSaidaBytesPortas(cen,tes,num_arq):
    teste = tes # 0 = Sem Iperf, 1 = 1Iperf, 2 = 2Iperf
    pasta = ''
    cenario = cen #1 , 2 ou 3
    s1_tx1 = [] #Porta 1 do Switch 1
    s1_tx2 = [] #Porta 2 do Switch 1
    s1_tx3 = [] #Porta 3 do Switch 1
    s3_rx1 = [] #Porta 1 do Switch 3
    s3_rx2 = [] #Porta 2 do Switch 3
    if teste == '0':
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/SemIperf/'
        #print('Sem Iperf')
    elif teste == '1':
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/1Iperf/'
        #print('1 Iperf')
    else:
        pasta = path_home+'/ryu/Bruno/Resultados/Cenario'+cenario+'/2Iperf/'
        #print('2 Iperf')
    #for j in range (0,30):
    arq = open(pasta+'teste'+num_arq+'.txt', 'r')
    #print('Path Arq: '+pasta+'teste'+num_arq+'.txt')
    texto = arq.readlines()
    somatorio_tx1 = 0
    somatorio_tx2 = 0
    somatorio_tx3 = 0
    somatorio_rx1 = 0
    somatorio_rx2 = 0
    for i in texto:
        vet = i.split(' ')
        vet[0] = vet[0].replace('s3->rx1:','')
        vet[1] = vet[1].replace('s3->rx2:','')
        vet[2] = vet[2].replace('s1->tx1:','')
        vet[3] = vet[3].replace('s1->tx2:','')
        vet[4] = vet[4].replace('s1->tx3:','')
        vet[4] = vet[4].replace('\n','')
        somatorio_tx1 = somatorio_tx1 + float(vet[2])
        somatorio_tx2 = somatorio_tx2 + float(vet[3])
        somatorio_tx3 = somatorio_tx3 + float(vet[4])
        somatorio_rx1 = somatorio_rx1 + float(vet[0])
        somatorio_rx2 = somatorio_rx2 + float(vet[1])
    arq.close()
    return somatorio_tx1,somatorio_tx2,somatorio_tx3,somatorio_rx1,somatorio_rx2

def RetornaMediaSaidaPortasBytesPortas(cen,tes):
    somatorio_tx1 = 0
    somatorio_tx2 = 0
    somatorio_tx3 = 0
    somatorio_rx1 = 0
    somatorio_rx2 = 0
    for i in range(0,30):
        aux_tx1 = 0
        aux_tx2 = 0
        aux_tx3 = 0
        aux_rx1 = 0
        aux_rx2 = 0
        aux_tx1,aux_tx2,aux_tx3,aux_rx1,aux_rx2 = RetornaSaidaBytesPortas(cen,tes,str(i+1))
        somatorio_tx1 = somatorio_tx1 + aux_tx1
        somatorio_tx2 = somatorio_tx2 + aux_tx2
        somatorio_tx3 = somatorio_tx3 + aux_tx3
        somatorio_rx1 = somatorio_rx1 + aux_rx1
        somatorio_rx2 = somatorio_rx2 + aux_rx2
    return somatorio_tx1/30,somatorio_tx2/30,somatorio_tx3/30,somatorio_rx1/30,somatorio_rx2/30

#print(RetornaMediaSaidaPortasBytesPortas('3','2'))
#print(RetornaSaidaBytesPortas('3','2','1'))
#RetornaVetoresComMedias('3','2')
#RetornaVetoresArquivos('0','1','1')
