#!/usr/bin/python
#Aplicacao servidor - Versao 7.0

import sys
import os
import socket
import pickle
import time

from scapy.all import *
#from rsvpserver import Rsvpserver

host = ''						#Servidor escutando em todas as portas
#port = int(sys.argv[1])				#Porta do servidor obtida atraves da CLI
port = 23000						#Porta do servidor obtida atraves da CLI
'''
filetest = 'testfile3.mov'				#Arquivo de teste
filename = '/home/bruno/pox/ext/classes.conf'	#Arquivo de lista de objetos Classe
'''
#Carregamento dos dados do arquivo de teste em memoria
'''filet = open(filetest,'r+b')
bytes = filet.read()
filet.close
'''
'''
#Carregamento da lista de objetos Classe
classlist = []
if os.path.isfile(filename):
	filec = open(filename,'rb')
	classlist = pickle.load(filec)
	filec.close()
'''
#Inicio da conexao
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))

sock.listen(5)
print 'Servidor escutando porta',port

conn,addr = sock.accept()
print 'Conectado com',addr

while True:
	#qos = 0

	#Recebimento do tipo de aplicacao
	data = conn.recv(4096)
	msg = str(data)

	print 'Mensagem recebida:',msg
	if msg!='FIN':
		conn.sendall('Recebida!')
		recv = msg.split('/')
		#Salvo um arquivo com os dados!!
		arq = open('/home/bruno/ryu/Bruno/Dados_QoS_Servidor.txt','w')
		#Formato a ser guardado = IP/Porta/Servico
		p = str(addr[0])+'/'+recv[1]+'/'+recv[0]
		print(p)
		arq.write(str(addr[0])+'/'+recv[1]+'/'+recv[0])
		arq.close()

		#Enviando um pacote ao servidor avisando sobre a atualizacao do arquivo
		dest = '10.0.0.99'
		destport = '1234'
		ip = IP(dst=dest)
		udp = UDP(dport=int(destport),sport=40000)
		pkt = ip/udp
		t = sr(pkt)
		print(t)
		#Fim do Envio


	else:
		print('Encerrando Conexao')
		conn.sendall('FIN')
		break

#Encerramento da conexao
print 'Encerrando conexao'
conn.close()
sock.close()
