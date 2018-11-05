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
		#recv = msg.split('/')
		recv = msg.split('/')
		#Salvo um arquivo com os dados!!
		arq = open('/home/bruno/ryu/Bruno/Dados_QoS_Servidor.txt','w')
		#Formato a ser guardado = IP/Porta/Servico
		#p = str(addr[0])+'/'+str(addr[1])+'/'+recv[0] #Porta que abriu a coxexao com HOST
		p = str(addr[0])+'/'+str(recv[1])+'/'+recv[0] #Porta que foi dita pelo host
		print(p)
		arq.write(str(addr[0])+'/'+recv[1]+'/'+recv[0]) #Guarda a porta que foi enviada pelo host
		#arq.write(str(addr[0])+'/'+str(addr[1])+'/'+recv[0]) #Guarda a porta que o socket abriu
		arq.close()

		#Enviando um pacote ao servidor avisando sobre a atualizacao do arquivo
		'''
		dest = '10.0.0.99'
		destport = '1234'
		ip = IP(dst=dest)
		udp = UDP(dport=int(destport),sport=40000)
		pkt = ip/udp
		t = sr(pkt)
		print(t)
		#Fim do Envio
		'''
		#Abre o VLC para iniciar o envio do video
		time.sleep(5)
		os.system('(sleep 140;echo "quit") | vlc --intf rc /home/bruno/teste_1080p.mp4 --sout udp://'+str(addr[0])+':'+str(recv[1])+' &') #Com QoS Video 1080p
		#os.system('ffmpeg -r 25 -i /home/bruno/teste_1080p.mp4 -c:v libx265 -x265-params crf=23 -strict experimental -f mjpeg udp://'+str(addr[0])+':'+str(recv[1])+' &')
		#os.system('vlc -vvv /home/bruno/teste_1080p.mp4 --sout udp://'+str(addr[0])+':'+str(recv[1])+' vlc://quit &') #Com QoS Video 1080p
		#os.system('(sleep 140;echo "quit") | vlc --intf rc /home/bruno/teste_720p2.mp4 --sout udp://'+str(addr[0])+':'+str(recv[1])+' &') #Com QoS Video 720p
		#os.system('(sleep 140;echo "quit") | vlc --intf rc /home/bruno/teste_1080p.mp4 --sout udp://'+str(addr[0])+':'+str(addr[1])+' &') #Sem QoS
		time.sleep(209)
		#os.system('(sleep 5;echo "stats";sleep 3;echo "shutdown") | telnet 10.0.0.1 '+str(recv[1])+' > /home/bruno/ryu/Bruno/StaticsVideo.txt')

		#Teste de destruir as qos
		#time.sleep(10)
		#os.system('ovs-vsctl -- --all destroy Queue')
		#Fim do Envio do Video


	else:
		#print('vlc --intf rc /home/bruno/ryu/Bruno/video_teste.mp4 --sout udp://'+str(addr[0])+':'+str(addr[1])+' &')
		print('vlc -vvv /home/bruno/teste_1080p.mp4 --sout udp://'+str(addr[0])+':'+str(recv[1])+' vlc://quit &')
		print('Encerrando Conexao')
		conn.sendall('FIN')
		break

#Encerramento da conexao
print 'Encerrando conexao'
conn.close()
sock.close()
