import os
path_home = os.getenv("HOME") #Captura o caminho da pasta HOME
for j in range (0,19):
    lista = []
    arq = open(path_home+'/ryu/Bruno/Resultados/Cenario1/SemIperf/teste'+str(j+1)+'.txt', 'r')
    texto = arq.readlines()
    print(len(texto))
    for i in range (len(texto)):
        if i%2 != 0:
            lista.append(texto[i])
    arq.close()
    arq = open(path_home+'/ryu/Bruno/Resultados/Cenario1/SemIperf/teste'+str(j+1)+'.txt', 'w')
    arq.writelines(lista)
    arq.close()
