APROX = 2

valor_envio= 6709.46

valor_recebimento= 918

#valor_entrada_iperf = 192.6

#Regra de 3
Resultado = (valor_recebimento * 100) / valor_envio
print('Resultado da regra de 3 :'+str(Resultado))
print("Valor da perda: "+str(round((100 - Resultado),APROX))+'%')
