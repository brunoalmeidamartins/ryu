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
import os

import requests

class MeuApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MeuApp, self).__init__(*args, **kwargs)
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
        print(mod)

    '''
    Instala regras na inicializacao
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        print('------------------------------------------')
        print('Dentro do Evento Inicial!!')
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
            r = requests.put('http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr','"tcp:127.0.0.1:6632"')
            r2 = requests.put('http://localhost:8080/v1.0/conf/switches/0000000000000002/ovsdb_addr','"tcp:127.0.0.1:6632"')
            print('Cheguei aqui!!')
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
            os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst=1234,actions=output:controller')
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
        '''
        msg = ev.msg
        datapath = msg.datapath
        id_switch = datapath.id
        if id_switch == 1:
            #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"port":'+str(ofproto.OFPP_CONTROLLER)+'}]}')
            #r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"port":1}]}')
            r3 = requests.post('http://localhost:8080/stats/flowentry/add','{"dpid":1,"priority":2,"match": {"udp_dst": "5002"}, "actions":[{"type":"OUTPUT","port":1}]}')

            print(r3.text)
        #print('Deu certo!!')
        '''
        '''
        msg = ev.msg
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        print(str(src)+' -> '+str(dst))
        '''
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        #print(dir(parser))
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            self.logger.info("Pacote LLDP")
            return
        if not pkt_ethernet:
            self.logger.info("Pacote Nao Sei!!")
            return
        pkt_arp = pkt.get_protocol(arp.arp)
        if pkt_arp:
            self.logger.info("Pacote ARP")
            return
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        if pkt_icmp:
            #self._handle_icmp(datapath, port, pkt_ethernet, pkt_ipv4, pkt_icmp)
            self.logger.info("Pacote ICMP")
            return
        if pkt_ipv4:
            #(pkt_ipv4)
            if pkt_ipv4.proto == 17:
                print('Esse pacote eh UDP!!')
            else:
                print('Esse pacote nao eh UDP!!!')
            self.logger.info("Pacote IPV4")

            t = pkt.get_protocol(udp.udp)
            if t:
                print("Agora sim!!")
                print(t)

            return


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
