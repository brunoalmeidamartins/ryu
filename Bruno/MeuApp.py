from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
#Pacotes
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
#Extras
from ryu.lib.dpid import dpid_to_str
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY
from ryu.lib.mac import haddr_to_bin
#Topologia
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
import networkx as nx
#Sistema
import os
import requests
import pickle
from classe import Classe

'''
Itens copiado do l3-qos-> Alexandre
'''
##### Porta do servidor
SERVER_PORT = 23000

##### Vazao maxima da rede (bps)
TX_MAX = 1000000000

#Ip de comunicacao com Controlador
IP_SERVER_QoS = '10.0.0.99'

#MAC do Controlador
MAC_SERVER_QoS = 'ff:ff:ff:00:00:00'

#Id do Switch onde esta os Servidores
ID_SWITCH = 3

#Porta que vai gerar o Packet_In
PORTA_Packet_In = 1234

#Mapeamento id em dpid
table_id = []

#Teste da Topologia
TABLE_MAC_SWITCH = []
#link_list = []

#Tabelas
TABELA_IP_SWITCH = [] #Mapea a saida do IP para cada switch
TABELA_MAC_SWITCH = [] #Mapea a saida de MAC para cada switch

#Arquivos
filename = '/home/bruno/ryu/Bruno/classes.conf'	#Arquivo de lista de objetos Classe

class MeuApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MeuApp, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self
        #self.net=nx.DiGraph()
        self.nodes = {}
        self.links = {}
        self.no_of_nodes = 0
        self.no_of_links = 0


    '''
    Envia a mensagem ao switch
    '''
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
        #print(mod)

    '''
    Instala regras na inicializacao
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        #print('------------------------------------------')
        #print('Dentro do Evento Inicial!!')
        """Handle switch features reply to remove flow entries in table 0 and 1."""
        msg = ev.msg
        datapath = msg.datapath
        '''
        Apaga Regras do switch
        '''
        [self.remove_flows(datapath, n) for n in [0, 1]]
        '''
        Fim Apaga Regras
        '''
        '''
        Envia Regra de Packet_In para os switches
        '''
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER,
                                          max_len=ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(type_=ofproto.OFPIT_APPLY_ACTIONS,
                                             actions=actions)]
        #match = parser.OFPMatch()
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=0,
                                match=parser.OFPMatch(),
                                instructions=inst)
        datapath.send_msg(mod)
        #print(mod)
        '''
        Fim Regra de Packet_In para os switches
        '''

        '''
        Area de testes
        '''
        try:
            #print('Cheguei aqui!!')
            #O processo faz um mapeamento de id em dpid
            tamanho_num = len(str(datapath.id))
            dpid_mont = ''
            for i in range(0,(16-tamanho_num)):
                dpid_mont = dpid_mont+'0'
            dpid_mont = dpid_mont+str(datapath.id)
            table_id.append([datapath.id,dpid_mont])
            #Insere ovs-manager em cada Switch para o REST
            r = requests.put('http://localhost:8080/v1.0/conf/switches/'+dpid_mont+'/ovsdb_addr','"tcp:127.0.0.1:6632"')
            #r2 = requests.put('http://localhost:8080/v1.0/conf/switches/0000000000000002/ovsdb_addr','"tcp:127.0.0.1:6632"')

            #r3 = requests.post('http://localhost:8080/qos/rules/0000000000000001','{"match": {tp_dst": "5002"}, "actions":{"port":'+str(ofproto.OFPP_CONTROLLER)+'}}')
            #r4 = requests.post('http://localhost:8080/qos/rules/0000000000000002','{"match": {tp_dst": "5002"}, "actions":{"port":'+str(ofproto.OFPP_CONTROLLER)+'}}')
            #r3 = requests.get('http://localhost:8080/stats/switches') #Pega todos os switches
            #r3 = requests.get('http://localhost:8080/stats/desc/1')
            #r3 = requests.get('http://localhost:8080/stats/flowdesc/1')
            #id_switch = datapath.id
            #if id_switch == 1:
                #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"port":'+str(ofproto.OFPP_CONTROLLER)+'}]}')
                #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"port":1}]}')
                #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"type":"OUTPUT","port":1}]}')

                #print(r3.text)
            #else:
                #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":2,"priority":2,"match": {"tp_dst": "5002"}, "actions":{"port":'+str(ofproto.OFPP_CONTROLLER)+'}}')
            #print(r3)
            #print('Terminei aqui!!')
            '''
            Regra de Packet In para QoS
            '''
            id_switch = datapath.id
            os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst='+str(PORTA_Packet_In)+',actions=output:controller')
            '''
            Fim Regra de Packet In para QoS
            '''
        except Exception as e:
            print(e)

        #print(r.text)
        '''
        Fim area de testes
        '''
        #print(mod)
        #print('------------------------------------------')
        #print(' ')
    '''
    Area do Packet_In
    '''
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        #Tipos de pacotes
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_udp = pkt.get_protocol(udp.udp)


        #Preenche as tabelas de IP e MAC
        #self.preencheTabelaIP(pkt)
        #self.preencheTabelaMAC(pkt)


        #Pacote ethernet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            #self.logger.info("Pacote LLDP")
            return
        if not pkt_ethernet:
            #self.logger.info("Pacote Nao Sei!!")
            return



        #Se for pacote ARP
        if pkt_arp:
            #Armazena tabela host->switch->porta
            dst = eth.dst
            src = eth.src
            dpid = datapath.id
            porta_host = msg.match['in_port'] #Porta onde gerou o evento
            lista_comparacao = []
            src_ip = pkt_arp.src_ip
            for i in TABLE_MAC_SWITCH:
                lista_comparacao.append(i[0])
            if str(src) not in lista_comparacao:
                TABLE_MAC_SWITCH.append([str(src),dpid,porta_host]) #Preenche a tabela de MAC
                TABELA_IP_SWITCH.append([str(src_ip),str(src)]) #Preenche a tabela de IPs->MAC
                #print('------------------')
                #print('Tabela onde esta o HOST')
                #print(TABLE_MAC_SWITCH)
                #print('IP HOST -> MAC HOST')
                #print(TABELA_IP_SWITCH)
                #print('------------------')
            lista_comparacao2 = []
            for i in TABELA_MAC_SWITCH:
                lista_comparacao2.append(str(i[0])+str(i[1]))
            comp = str(src)+str(dpid)
            if comp not in lista_comparacao2:
                TABELA_MAC_SWITCH.append([str(src),dpid,porta_host])
                #print('------------------')
                #print('Tabela de mapeamento switch->Saida')
                #print(TABELA_MAC_SWITCH)
                #print('------------------')



            if str(pkt_arp.dst_ip) == IP_SERVER_QoS: #Enviar ARP response com o MAC
                #print('Responder o arp com MAC do Servidor')
                if pkt_arp.opcode == arp.ARP_REQUEST:
                    #print('Quer o ARP do servidor_QoS')
                    port1 = msg.match['in_port']
                    pkt = packet.Packet()
                    pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype,
                                                       dst=pkt_ethernet.src,
                                                       src=MAC_SERVER_QoS))
                    pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY,
                                             src_mac=MAC_SERVER_QoS,
                                             src_ip=IP_SERVER_QoS,
                                             dst_mac=pkt_arp.src_mac,
                                             dst_ip=pkt_arp.src_ip))
                    self._send_packet(datapath, port1, pkt)
            return





        #Se for ICMP
        if pkt_icmp:
            #self._handle_icmp(datapath, port, pkt_ethernet, pkt_ipv4, pkt_icmp)
            #self.logger.info("Pacote ICMP")
            return

        #Se for IPv4
        if pkt_ipv4:
            if pkt_udp:
                if pkt_udp.dst_port == 1234:
                    #print("UDP na Porta 1234")
                    if pkt_ipv4.dst == IP_SERVER_QoS:
                        #Responde o Pacote UDP Vindo!!
                        #print('Eh para o servidor QoS... Responnder')
                        pkt2 = pkt.get_protocol(ethernet.ethernet)
                        port1 = msg.match['in_port']
                        pkt_resp = packet.Packet()
                        e = ethernet.ethernet(ethertype=pkt2.ethertype,dst=pkt_ethernet.src,src=MAC_SERVER_QoS) #Parte da camada Rede
                        i = ipv4.ipv4(dst=pkt_ipv4.src,src=IP_SERVER_QoS,proto=17) #Parte do IP
                        u = udp.udp(dst_port=pkt_udp.src_port,src_port=1234) #Parte do UDP
                        pkt_resp = e/i/u #Monta o pacote
                        self._send_packet(datapath, port1, pkt_resp)
                        #print('Pacote respondido!!!')
                        #Fim da resposta do Pacote UDP!!

                        #Verificando os dados Gravados no arquivo!!
                        #Somente para o Swtich onde esta os Servidores
                        if datapath.id == ID_SWITCH:
                            arq = open('/home/bruno/ryu/Bruno/Dados_QoS_Servidor.txt','r')
                            #arq = open('/home/administrador/ryu/Bruno/Dados_QoS_Servidor.txt','r')
                            texto = arq.read()
                            #print('-----------------------')
                            #print(texto)
                            #'10.0.0.2'/25000/video
                            arq.close()
                            texto1 = texto.split('/')
                            ip_client = texto1[0]
                            porta_envio = texto1[1]
                            servico_fornecido = texto1[2]
                            ip_server = pkt_ipv4.src
                            #print("Ip Client: "+ip_client)
                            #print("Ip Server: "+ip_server)
                            #print("Porta Envio: "+porta_envio)
                            #print("Servico: "+servico_fornecido)
                            #print('-----------------------')

                            '''
                            Montagem das regras
                            '''
                            grafo = nx.MultiGraph()
                            #Obtem os switches
                            switch_list = get_switch(self.topology_api_app, None)
                            TABELA_SWITCH=[switch.dp.id for switch in switch_list]
                            #print(TABELA_SWITCH)

                            #Obtencao dos links 'Ida e Volta'
                            links_list = get_link(self.topology_api_app, None)
                            links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
                            links=[(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]
                            #Monta o grafo para calcular a rota entre Server e Client
                            index = 0
                            for i in links:
                                grafo.add_edge(i[0],i[1],cost=1,index=index)
                                index = index +1
                            #print(nx.dijkstra_path(grafo,3,1,weight='cost'))
                            index = 0
                            ip = ''
                            for i in TABLE_MAC_SWITCH:
                                for j in TABELA_IP_SWITCH:
                                    if j[1] == i[0]:
                                        ip = j[0]
                                        break
                                grafo.add_edge(ip,i[1],cost=1,index=index)
                            #print('******************PATH************************')
                            #print(nx.dijkstra_path(grafo,'10.0.0.1','10.0.0.3',weight='cost'))
                            #Fim Montagem grafo
                            print('***************Path Server->Client**********************')
                            print(nx.dijkstra_path(grafo,ip_server,ip_client,weight='cost'))
                            path_server_client = nx.dijkstra_path(grafo,ip_server,ip_client,weight='cost')
                            print('***************Path Client->Server***********************')
                            print(nx.dijkstra_path(grafo,ip_client,ip_server,weight='cost'))
                            path_client_server = nx.dijkstra_path(grafo,ip_client,ip_server,weight='cost')

                            #Regras
                            mac_server = ''
                            mac_client = ''
                            for i in TABELA_IP_SWITCH:
                                if i[0] == ip_client:
                                    mac_client = i[1]
                                if i[0] == ip_server:
                                    mac_server = i[1]
                            print('mac_cliente: '+mac_client)
                            print('mac_server: '+mac_server)
                            #Aplica QoS nas portas
                            qos = os.popen("ovs-vsctl list qos | grep _uuid | awk '{print $3}'").read().strip('\n')
                            #Excluo a primeira posicao e a ultima, pois sao os IPs
                            for i in range(1,len(path_server_client)-1):
                                switch_caminho = path_server_client[i]
                                porta_switch = ''
                                for j in TABELA_MAC_SWITCH:
                                    if j[1] == switch_caminho:
                                        porta_switch = j[2]
                                        break
                                os.system('ovs-vsctl set port s'+str(switch_caminho)+'-eth'+str(porta_switch)+' qos='+str(qos))
                                #print('ovs-vsctl set port s'+str(switch_caminho)+'-eth'+str(porta_switch)+' qos='+str(qos))

                                #os.system('ovs-vsctl set port r%d-eth%d qos=%s' %(dpid,prt,qos))

                            #Acha qual fila eh a QoS pedida
                            #Carregamento da lista de objetos Classe
                            classlist = []
                            if os.path.isfile(filename):
                            	filec = open(filename,'rb')
                            	classlist = pickle.load(filec)
                            	filec.close()
                            fila_saida = '0' #Fila a ser aplicada
                            for c in classlist:
                                if c.nome == servico_fornecido:
                                    fila_saida = c.id
                            print('Fila saida: '+str(fila_saida))


                            #Aplica a regra de saida QoS
                            for i in range(1,len(path_server_client)-1):
                                switch_caminho = path_server_client[i]
                                porta_switch = ''
                                for j in TABELA_MAC_SWITCH:
                                    if j[1] == switch_caminho:
                                        porta_switch = j[2]
                                        break
                                #os.system('ovs-ofctl add-flow s' + str(switch_caminho) + ' priority=40000,dl_type=0x0800,nw_dst='+str(ip_client)+',nw_proto=17,idle_timeout=60,tp_dst='+str(porta_envio)+',actions=enqueue:'+str(porta_switch)+':'+str(fila_saida))
                                #print('ovs-ofctl add-flow s' + str(switch_caminho) + ' priority=40000,dl_type=0x0800,nw_dst='+str(ip_client)+',nw_proto=17,idle_timeout=60,tp_dst='+str(porta_envio)+',actions=enqueue:'+str(porta_switch)+':'+str(fila_saida))
                                #Teste tempo
                                os.system('ovs-ofctl add-flow s' + str(switch_caminho) + ' priority=40000,dl_type=0x0800,nw_dst='+str(ip_client)+',nw_proto=17,idle_timeout=5,tp_dst='+str(porta_envio)+',actions=enqueue:'+str(porta_switch)+':'+str(fila_saida))
                                print('ovs-ofctl add-flow s' + str(switch_caminho) + ' priority=40000,dl_type=0x0800,nw_dst='+str(ip_client)+',nw_proto=17,idle_timeout=5,tp_dst='+str(porta_envio)+',actions=enqueue:'+str(porta_switch)+':'+str(fila_saida))








                            '''
                            print('-----------------------------')
                            print('-------------Teste----------')
                            switch_list = get_switch(self.topology_api_app, None)
                            #switches=[switch.dp.id for switch in switch_list]
                            for i in switch_list:
                                print(i)

                            Link: Port<dpid=2, port_no=1, LIVE> to Port<dpid=1, port_no=5, LIVE>
                            Link: Port<dpid=1, port_no=5, LIVE> to Port<dpid=2, port_no=1, LIVE>
                            Link: Port<dpid=3, port_no=5, LIVE> to Port<dpid=2, port_no=2, LIVE>
                            Link: Port<dpid=2, port_no=2, LIVE> to Port<dpid=3, port_no=5, LIVE>



                            links_1 = get_link(self.topology_api_app, None)
                            for i in links_1:
                                #Para cada i
                                #links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
                                a = str(i)
                                vet = a.split(',')
                                vet_aux = []
                                for t in range(0,len(vet)):
                                    if t == 4:
                                        pass
                                    else:
                                        vet_aux.append(vet[t])
                                vet = vet_aux
                                print(vet)
                                pass


                            print('-----------------------------')
                            print('-------------FIM Teste----------')
                            '''


                            #print(self.net)


                else:
                    #print("UDP!! Nao eh a porta 1234")
                    pass
                #if pkt_udp.
                #print(" ")
                #print(" ")
                #print(t)

            #return


        #dst = eth.dst
        #src = eth.src
        '''
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(
            datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        dp.send_msg(out)
        '''


    '''
    FIM Area do Packet_In
    '''

    '''
    Preenche as tabelas do IP_SwITCH e MAC_SWITCH
    '''
    '''
    def preencheTabelaIP(pkt):
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        if pkt_arp:
            pass
        elif pkt_icmp:
            pass
        elif pkt_ipv4:
            pass
        else:
            #Faz nada!!

    def preencheTabelaMAC(pkt):
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)

    '''
    '''
    FIM Preenche as tabelas do IP_SwITCH e MAC_SWITCH
    '''

    '''
    Apaga Regras Swithc
    '''
    def remove_flows(self, datapath, table_id):
        """Removing all flow entries."""
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        empty_match = parser.OFPMatch()
        instructions = []
        flow_mod = self.remove_table_flows(datapath, table_id,
                                        empty_match, instructions)
        #print "deleting all flow entries in table ", table_id
        datapath.send_msg(flow_mod)
    def remove_table_flows(self, datapath, table_id, match, instructions):
        """Create OFP flow mod message to remove flows from table."""
        ofproto = datapath.ofproto
        flow_mod = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, table_id,
                                                      ofproto.OFPFC_DELETE, 0, 0,
                                                      1,
                                                      ofproto.OFPCML_NO_BUFFER,
                                                      ofproto.OFPP_ANY,
                                                      OFPG_ANY, 0,
                                                      match, instructions)
        return flow_mod
    '''
    FIM Apaga Regras Swithc
    '''


    '''
    Envia Pacote para Host
    '''
    def _send_packet(self, datapath, port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt.serialize()
        #self.logger.info("packet-out %s" % (pkt,))
        data = pkt.data
        actions = [parser.OFPActionOutput(port=port)]
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions,
                                  data=data)
        datapath.send_msg(out)
    '''
    FIM Envia Pacote para Host
    '''

    '''
    Monta topologia #Codigo copiado do Site:
    https://sdn-lab.com/2014/12/25/shortest-path-forwarding-with-openflow-on-ryu/
    https://github.com/osrg/ryu/pull/29/commits/4487c9272e69ab93139baf6a2ee48f3b31bb4f02
    https://github.com/castroflavio/ryu
    '''
    @set_ev_cls(event.EventSwitchEnter)
    def get_topology_data(self, ev):
        switch_list = get_switch(self.topology_api_app, None)
        switches=[switch.dp.id for switch in switch_list]
        #self.net.add_nodes_from(switches)
        links_list = get_link(self.topology_api_app, None)

        links=[(link.src.dpid,link.dst.dpid,{'port':link.src.port_no}) for link in links_list]
        #self.net.add_edges_from(links)
        links=[(link.dst.dpid,link.src.dpid,{'port':link.dst.port_no}) for link in links_list]
        #self.net.add_edges_from(links)
        #print('-------------------------')
        #print('**************Switches****************')
        #print(switches)
        #print('**************Links****************')
        #print(links)
        #print('-------------------------')
        #print('**************Links_list_teste****************')
        #for i in links_list:
            #print(i)
        #print('-------------------------')
        #print "**********List of links"
        #print self.net.edges()
    '''
    Fim Monta topologia
    '''


#Tudo o que eu quiser iniciar, basta colocar aqui!!
#Require
app_manager.require_app('ryu.app.ofctl_rest')
app_manager.require_app('ryu.app.simple_switch_13_mod')
app_manager.require_app('ryu.app.rest_conf_switch')
app_manager.require_app('ryu.app.rest_topology')
#app_manager.require_app('ryu.app.rest_qos_mod')
