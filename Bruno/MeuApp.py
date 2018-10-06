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
#import networkx as nx
#Sistema
import os
import requests

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
TABELA_SWITCH = []
TABELA_IP_SWITCH = [] #Mapea a saida do IP para cada switch
TABELA_MAC_SWITCH = [] #Mapea a saida de MAC para cada switch

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
        print('------------------------------------------')
        print(' ')
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
            for i in TABLE_MAC_SWITCH:
                lista_comparacao.append(i[0])
            if str(src) not in lista_comparacao:
                TABLE_MAC_SWITCH.append([str(src),dpid,porta_host])
                print('------------------')
                print('Tabela onde esta o HOST')
                print(TABLE_MAC_SWITCH)
                print('------------------')
            lista_comparacao2 = []
            for i in TABELA_MAC_SWITCH:
                a = i[0].replace(':','')
                b = a + str(i[1]) + str(i[2])
                c = int(b)
                lista_comparacao2.append(c)
            d = str(src).replace(':','')
            e = d + str(dpid) + str(porta_host)
            f = int(e)
            if f not in lista_comparacao2:
                TABELA_MAC_SWITCH.append([str(src),dpid,porta_host])
                print('------------------')
                print('Tabela de mapeamento switch->Saida')
                print(TABELA_MAC_SWITCH)
                print('------------------')



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
                            texto = arq.read()


                            print('-----------------------')
                            print(texto)
                            arq.close()
                            print('-----------------------')

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
                    print("UDP!! Nao eh a porta 1234")
                #if pkt_udp.
                print(" ")
                print(" ")
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
        print "deleting all flow entries in table ", table_id
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
        print('-------------------------')
        print('**************Switches****************')
        print(switches)
        print('**************Links****************')
        print(links)
        print('-------------------------')
        print('**************Links_list_teste****************')
        for i in links_list:
            print(i)
        print('-------------------------')
        #print "**********List of links"
        #print self.net.edges()

        #Tabela de Switch recebe os Switches que existem
        TABELA_SWITCH = switches
    '''
    Fim Monta topologia
    '''


#Tudo o que eu quiser iniciar, basta colocar aqui!!
#Require
app_manager.require_app('ryu.app.ofctl_rest')
app_manager.require_app('ryu.app.simple_switch_13_mod')
app_manager.require_app('ryu.app.rest_conf_switch')
app_manager.require_app('ryu.app.rest_topology')
