#!/usr/bin/python
#Aplicacao cliente - Versao 7.0

import sys
import socket
import os
import time
#from rsvpclient import Rsvpclient

#host = sys.argv[1]			#Endereco do servidor remoto obtido atraves da CLI
host = '10.0.0.8'			#Endereco do servidor remoto obtido atraves da CLI
#port = int(sys.argv[2])		#Porta do servidor remoto obtida atraves da CLI
port = 23000				#Porta do servidor remoto obtida atraves da CLI
#filetest = 'test.mov'			#Arquivo de teste
qos = False				#A principio, classe de servico nao disponivel
'''
output=open('resultados-sessao3-rodada3.txt','ab')
outputo=open('overhead-sessao3-rodada3.txt','ab')
'''
#Inicio da conexao
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))

#Abertura do arquivo de teste
'''
if os.path.isfile(filetest):
	os.remove(filetest)
filet = open(filetest,'w+b')
'''
cond = 2
while cond != 0:
	#Envio do tipo de aplicacao
	#if not qos:

	#msg = raw_input('Informe o conteudo: ')
	if cond == 2:
		porta_servico = '25000'
		#msg = 'video/25000'
		msg = 'video'
		msg = msg +'/'+porta_servico
	else:
		#Antes de Enviar a msg FIM abre o aguarda o vlc
		#os.system('vlc -I rc --rc-host 10.0.0.1:'+porta_servico+' udp://@10.0.0.1:'+porta_servico+' &')
		#print("Recebendo Video!!!")
		time.sleep(210) #Aguarda o tempo do video 2:20 ou 140
		#Fim do aguardo do vlc
		msg = 'FIN'
		#begin=time.time()
	sock.sendall(msg)

	#Resposta do servidor
	data = sock.recv(4096)
	msg_rec = str(data)
	print(msg_rec)
	cond = cond-1
	if msg_rec == 'FIN':
		#cond = 0
		pass
#Encerramento da conexao
print 'Encerrando conexao'
sock.close()
