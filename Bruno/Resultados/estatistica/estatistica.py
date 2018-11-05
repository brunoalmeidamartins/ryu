#!/usr/bin/python
#Aplicacao que reune diversas funcoes estatisticas - Versao 01/07/18

import sys
import math
import numpy as np
from matplotlib import pyplot as pl
from grafico import desenha

APROX = 2			#Numero de casas decimais para aproximacao

#Calculo da media
def media(L):
	soma=0.0
	for i in L:
		soma+=i
	return soma/len(L)

#Calculo da variancia
def variancia(L):
	soma=0.0
	x=media(L)
	for i in L:
		soma+=((i-x)**2)
	return soma/(len(L)-1)

#Calculo do desvio padrao
def desvioPadrao(L):
	return math.sqrt(variancia(L))

#Calculo do coeficiente de variacao
def cv(L):
	return desvioPadrao(L)/media(L)

#Calculo da covariancia
def covariancia(L1,L2):
	cov=0
	for i in range(len(L1)):
		cov+=(L1[i]-media(L1))*(L2[i]-media(L2))
	return cov

#Calculo da correlacao
def correlacao(L1,L2):
	return covariancia(L1,L2)/(desvioPadrao(L1)*desvioPadrao(L2))

#Calculo do intervalo de confianca
def ic(L,tabela):
	intervalo=[]
	x=media(L)
	erroPadrao=desvioPadrao(L)/math.sqrt(len(L))
	#tabela=raw_input('Digite o valor da tabela t/z para %d graus de liberdade: ' %(len(L)-1))
	liminf=x-(float(tabela)*erroPadrao)
	limsup=x+(float(tabela)*erroPadrao)
	intervalo.append(round(liminf,APROX))	
	intervalo.append(round(limsup,APROX))
	return intervalo

#Calculo do Teste T
def icTesteT(L1,L2):
	intervalo=[]
	x1=media(L1)
	x2=media(L2)
	ep1=variancia(L1)/len(L1)
	ep2=variancia(L2)/len(L2)
	s=math.sqrt(ep1+ep2)
	numeradorv=(ep1+ep2)**2
	denominadorv=((ep1**2/(len(L1)+1))+(ep2**2/(len(L2)+1)))
	v=(numeradorv/denominadorv)-2
	tabela=raw_input('Digite o valor da tabela t para %f graus de liberdade: ' %v)
	intervalo.append((x1-x2)-(float(tabela)*s))	
	intervalo.append((x1-x2)+(float(tabela)*s))
	return intervalo

#Calculo das diferencas de amostras
def difAmostra(L1,L2):
	if len(L1)!=len(L2):
		print "Tamanhos de amostras diferentes"
		return
	dif=[]
	for i in range(len(L1)):
		dif.append(L1[i]-L2[i])
	return dif

#Calculo da regressao linear
def regressaoLinear(x,y):
	somatoriox = 0
	somatorioy = 0
	somatorioxy = 0
	somatoriox2 = 0
	SSY = 0
	somaestimate = 0
	somae = 0
	somae2 = 0

	n = len(x)						#Quantidade de amostras
	SS0 = n * media(y)**2					#Soma dos quadrados da media de y - SS0

	for i in range(n):
		somatoriox += x[i]				#Somatorio de x
		somatorioy += y[i]				#Somatorio de y
		somatorioxy += x[i] * y[i]			#Somatorio de x * y
		somatoriox2 += x[i]**2				#Soma dos quadrados de x
		SSY += y[i]**2					#Soma dos quadrados de y - SSY

	#Calculos das estimativas
	b1 = round((somatorioxy - n * media(x) * media(y)) / (somatoriox2 - n * (media(x)**2)),APROX)	#b1
	b0 = round(media(y) - (b1 * media(x)),APROX)							#b0

	for i in range(n):
		estimate = b0 + (b1 * x[i])			#Estimativa
		somaestimate += estimate			#Somatorio das estimativas
		e = y[i] - estimate				#Erro
		e2 = e**2					#Erro quadrado
		somae += e					#Soma dos erros
		somae2 += e2					#Soma dos erros quadrados

	SST = SSY - SS0						#Soma total dos quadrados - SST
	SSE = SSY - (b0 * somatorioy) - (b1 * somatorioxy)	#Soma dos erros quadrados (com regressao) - SSE

	#Calculos de R2 e Se
	R2 = 1 - (SSE / SST)					#Coeficiente de detelminacao - R2
	Se = math.sqrt(SSE / (n - 2))				#Desvio padrao de erros - Se

	#Calculos dos intervalos de confianca para regressoes
	Sb0 = round(Se * math.sqrt((1 / n) + (media(x)**2 / (somatoriox2 - (n * media(x)**2)))),APROX)
	Sb1 = round(Se / (math.sqrt(somatoriox2 - (n * media(x)**2))),APROX)

	tabela = float(raw_input('Digite o valor da tabela t/z para %d graus de liberdade: ' %(n - 2)))

	b0min = b0 - tabela * Sb0				#Calculo dos intervalos de confianca
	b0max = b0 + tabela * Sb0
	b1min = b1 - tabela * Sb1
	b1max = b1 + tabela * Sb1
	
	print 'Intervalo de confianca b0: %0.4f - %0.4f' %(b0min,b0max) 
	print 'Intervalo de confianca b1: %0.4f - %0.4f' %(b1min,b1max) 

	#Calculos dos intervalos de confianca para predicoes
	xp = int(raw_input('Digite o valor da amostra futura (Xp): '))
	m = 1
	yp = b0 + b1 * xp
	Sy = round(Se * math.sqrt((1 / m) + (1 / n) + (((xp - media(x))**2) / (somatoriox2 - (n * media(x)**2)))),APROX)
	
	ypmin = yp - tabela * Sy
	ypmax = yp + tabela * Sy
	print 'Intervalo de confianca previsto (Yp): %0.4f - %0.4f' %(ypmin,ypmax) 

	#Criacao dos graficos	
	pl.title('Regressao Linear')
	pl.xlim(0,max(x)+1)
	pl.ylim(0,max(y)+1)

	pl.plot(x,y,'o')

	x2=np.array([min(x),max(x)])
	y2=np.array([media(y),media(y)])
	pl.plot(x2,b0+b1*x2,'-')				#Regressao
	pl.plot(x2,y2,'-')					#Media

	pl.text(max(x)+0.2,media(y),'y')
	pl.text(0.2,max(y),'y=%0.4f+%0.4fx' %(b0,b1))
	pl.text(0.2,max(y)-0.5,'R2: %0.4f' %R2)
	pl.text(0.2,max(y)-1.0,'Se: %0.4f' %Se)
	pl.text(0.2,max(y)-1.5,'e: %0.4f' %somae)
	pl.text(0.2,max(y)-2.0,'e2: %0.4f' %somae2)

	pl.show()


#####Leitura de arquivos de resultados
input = open('stp-16x4.txt', 'r')
S5 = [float(foo) for foo in input.readlines()]
input.close()

input = open('stp-128x4.txt', 'r')
S10 = [float(foo) for foo in input.readlines()]
input.close()

input = open('stp-192x16.txt', 'r')
S15 = [float(foo) for foo in input.readlines()]
input.close()

input = open('stp-256x16.txt', 'r')
S20 = [float(foo) for foo in input.readlines()]
input.close()

input = open('traffic-16x4.txt', 'r')
T5 = [float(foo) for foo in input.readlines()]
input.close()

input = open('traffic-128x4.txt', 'r')
T10 = [float(foo) for foo in input.readlines()]
input.close()

input = open('traffic-192x16.txt', 'r')
T15 = [float(foo) for foo in input.readlines()]
input.close()

input = open('traffic-256x16.txt', 'r')
T20 = [float(foo) for foo in input.readlines()]
input.close()

input = open('ecmp-16x4.txt', 'r')
E5 = [float(foo) for foo in input.readlines()]
input.close()

input = open('ecmp-128x4.txt', 'r')
E10 = [float(foo) for foo in input.readlines()]
input.close()

input = open('ecmp-192x16.txt', 'r')
E15 = [float(foo) for foo in input.readlines()]
input.close()

input = open('ecmp-256x16.txt', 'r')
E20 = [float(foo) for foo in input.readlines()]
input.close()

input = open('isolated-16x4.txt', 'r')
I5 = [float(foo) for foo in input.readlines()]
input.close()

input = open('isolated-128x4.txt', 'r')
I10 = [float(foo) for foo in input.readlines()]
input.close()

input = open('isolated-192x16.txt', 'r')
I15 = [float(foo) for foo in input.readlines()]
input.close()

input = open('isolated-256x16.txt', 'r')
I20 = [float(foo) for foo in input.readlines()]
input.close()

#####Valores de tabelas T/Z
tam = len(S5)

if tam > 30:
	tab = '1.96'
if tam == 30:
	tab = '2.045'
if tam == 25:
	tab = '2.064'
if tam == 20:
	tab = '2.093'
if tam == 15:
	tab = '2.145'
	
#tab='1.645'	#>30 90%
#tab='1.699'	#30 90%
#tab='1.711'	#25 90%
#tab='1.729'	#20 90%
#tab='1.761'	#15 90%

#####Medias
ms5=round(media(S5),APROX)
ms10=round(media(S10),APROX)
ms15=round(media(S15),APROX)
ms20=round(media(S20),APROX)

me5=round(media(E5),APROX)
me10=round(media(E10),APROX)
me15=round(media(E15),APROX)
me20=round(media(E20),APROX)

mt5=round(media(T5),APROX)
mt10=round(media(T10),APROX)
mt15=round(media(T15),APROX)
mt20=round(media(T20),APROX)

mi5=round(media(I5),APROX)
mi10=round(media(I10),APROX)
mi15=round(media(I15),APROX)
mi20=round(media(I20),APROX)

#####Intervalos de Confianca
is5=ic(S5,tab)
is10=ic(S10,tab)
is15=ic(S15,tab)
is20=ic(S20,tab)

ie5=ic(E5,tab)
ie10=ic(E10,tab)
ie15=ic(E15,tab)
ie20=ic(E20,tab)

it5=ic(T5,tab)
it10=ic(T10,tab)
it15=ic(T15,tab)
it20=ic(T20,tab)

ii5=ic(I5,tab)
ii10=ic(I10,tab)
ii15=ic(I15,tab)
ii20=ic(I20,tab)

#####Impressao dos resultados
print '\n\nMedia STP 16x4: ',ms5
print 'IC STP 16x4: ',is5

print '\n\nMedia TRAFFIC 16x4: ',mt5
print 'IC TRAFFIC 16x4: ',it5

print '\n\nMedia ECMP 16x4: ',me5
print 'IC ECMP 16x4: ',ie5

print '\n\nMedia ISOLATED 16x4: ',mi5
print 'IC ISOLATED 16x4: ',ii5

print '\n\nMedia STP 128x4: ',ms10
print 'IC STP 128x4: ',is10

print '\n\nMedia TRAFFIC 128x4: ',mt10
print 'IC TRAFFIC 128x4: ',it10

print '\n\nMedia ECMP 128x4: ',me10
print 'IC ECMP 128x4: ',ie10

print '\n\nMedia ISOLATED 128x4: ',mi10
print 'IC ISOLATED 128x4: ',ii10

print '\n\nMedia STP 192x16: ',ms15
print 'IC STP 192x16: ',is15

print '\n\nMedia TRAFFIC 192x16: ',mt15
print 'IC TRAFFIC 192x16: ',it15

print '\n\nMedia ECMP 192x16: ',me15
print 'IC ECMP 192x16: ',ie15

print '\n\nMedia ISOLATED 192x16: ',mi15
print 'IC ISOLATED 192x16: ',ii15

print '\n\nMedia STP 256x16: ',ms20
print 'IC STP 256x16: ',is20

print '\n\nMedia TRAFFIC 256x16: ',mt20
print 'IC TRAFFIC 256x16: ',it20

print '\n\nMedia ECMP 256x16: ',me20
print 'IC ECMP 256x16: ',ie20

print '\n\nMedia ISOLATED 256x16: ',mi20
print 'IC ISOLATED 256x16: ',ii20

#####Geracao dos graficos
param1=[ms5,mt5,me5,mi5]
param2=[(is5[1]-is5[0])/2,(it5[1]-it5[0])/2,(ie5[1]-ie5[0])/2,(ii5[1]-ii5[0])/2]
desenha(param1,param2,50,'Trace 16 maps/4 reduces')

param1=[ms10,mt10,me10,mi10]
param2=[(is10[1]-is10[0])/2,(it10[1]-it10[0])/2,(ie10[1]-ie10[0])/2,(ii10[1]-ii10[0])/2]
desenha(param1,param2,200,'Trace 128 maps/4 reduces')

param1=[ms15,mt15,me15,mi15]
param2=[(is15[1]-is15[0])/2,(it15[1]-it15[0])/2,(ie15[1]-ie15[0])/2,(ii15[1]-ii15[0])/2]
desenha(param1,param2,200,'Trace 192 maps/16 reduces')

param1=[ms20,mt20,me20,mi20]
param2=[(is20[1]-is20[0])/2,(it20[1]-it20[0])/2,(ie20[1]-ie20[0])/2,(ii20[1]-ii20[0])/2]
desenha(param1,param2,350,'Trace 256 maps/16 reduces')
