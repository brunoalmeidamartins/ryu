#!/usr/bin/python
#Aplicacao servidor - Versao 7.0

import sys
import os
import socket
import pickle
import time
from rsvpserver import Rsvpserver

host = '10.0.0.99'						#Servidor escutando em todas as portas
#port = int(sys.argv[1])				#Porta do servidor obtida atraves da CLI
#port = 23000						#Porta do servidor obtida atraves da CLI
port = 1234
'''
filetest = 'testfile3.mov'				#Arquivo de teste
#filename = '/home/bruno/pox/ext/classes.conf'	#Arquivo de lista de objetos Classe
filename=os.getenv("HOME")+'/pox/ext/classes.conf'	#Nome do arquivo de classes de servicos

#Carregamento dos dados do arquivo de teste em memoria
filet = open(filetest,'r+b')
bytes = filet.read()
filet.close

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
	'''
	qos = 0

	#Recebimento do tipo de aplicacao
	data = conn.recv(4096)
	msg = str(data)

	print 'Mensagem recebida:',msg

	if msg!='FIN':
		for c in classlist:
			#Classe de servico disponivel
			if c.nome==msg:
				qos = 1
				conn.sendall('RSVP')
				Rsvpserver(addr[0],c.id).start()	#inicio do daemon RSVP servidor
				conn.sendall('vlc') #Enviando uma mensagem vlc
				os.system('(sleep 120;echo "quit") | vlc --intf rc /home/bruno/pox/ext/teste_1080p.mp4 --sout udp://10.0.1.1:23000 &')
				print 'Arquivo enviado'
				msg='FIN'
				break

	#Termino da conexao
	if msg=='FIN':
		break

	#Classe de servico nao disponivel
	if not qos:
		conn.sendall('ACK')
	'''
	time.sleep(60)
	break

#Encerramento da conexao
print 'Encerrando conexao'
conn.close()
sock.close()
