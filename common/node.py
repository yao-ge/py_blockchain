#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: node.py
# Created Time: 2019年10月31日 星期四 17时49分37秒
#########################################################################

from common import process_packet
from common import process_block
from common import edit_cfg
from common import config
import time

class Node:
    def __init__(self, port = 2231):
        self.port = port
        self.new_header_hash = '0' * 64
        self.headers_hash_list = []
        self.p = process_packet.Pro_pkt()
        self.pb = process_block.Pro_block()
        self.e = edit_cfg.Edit_cfg()

    def listen_from_port(self, sport = 0):
        #filter_rule = "udp dst port " + str(self.port) + " and src port " \
        #        + str(sport)
        filter_rule = "udp dst port " + str(self.port)
        return self.p.recv_pkt(filter_rule, 1)

    def get_request_type(self, sport = 0):
        pkt = self.listen_from_port(sport)
        if pkt[0]['Raw'].load.startswith(b'read'):
            request_type = 'read'
        elif pkt[0]['Raw'].load.startswith(b'write'):
            request_type = 'write'
        elif pkt[0]['Raw'].load.startswith(b'broadcast'):
            request_type = 'broadcast'
        elif pkt[0]['Raw'].load.startswith(b'exit'):
            request_type = 'exit'

        return request_type, pkt[0]['IP']

    def change_request_type(self, pkt, old_type, new_type):
        pkt.load = pkt.load.replace(old_type, new_type)
        return pkt

    def sr1_pkt_from_storage_to_user(self, request_pkt, dport = 0):
        pkt = request_pkt
        pkt.dport = dport
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()

        re_pkt = self.listen_from_port(dport)

        pre_header_hash, data_hash, timestamp, nonce = \
                self.pb.unpack_block(re_pkt[0]['IP'].load[:144])

        hash_str = "".join([pre_header_hash.decode(), data_hash.decode(),\
                str(timestamp), str(nonce)])

        self.new_header_hash = self.pb.gen_hash(hash_str)
        self.headers_hash_list.append(self.new_header_hash)
        return re_pkt[0]['IP']

    def send_pkt_to_storage(self, send_pkt, dport = 0):
        pkt = send_pkt
        pkt.dport = dport
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()

    def broadcast_to_all_nodes(self, pkt):
        node_count = self.e.count_cfg("node")
        dport_list = config.nodes_list[0 : count]
        self.p.broadcast_pkt(self.port, dport_list, pkt.load)

    def gen_pkt_with_pre_header_hash(self, sport = 0, dport = 0, \
            pre_header_hash = '0' * 64):
        pkt = self.p.construct_pkt_with_pre_header_hash(\
                sport, dport, pre_header_hash)
        self.new_header_hash = self.p.new_header_hash
        self.headers_hash_list.append(self.new_header_hash)
        return pkt

    def send_new_header_hash_to_user(self, sport = 0, dport = 0):
        pkt = self.p.construct_pkt(sport, dport, self.new_header_hash)
        self.p.pkt = pkt
        return self.p.send_pkt()
