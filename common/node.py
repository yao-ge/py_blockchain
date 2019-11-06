#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: node.py
# Created Time: 2019年10月31日 星期四 17时49分37秒
#########################################################################

from common import process_packet

class Node:
    def __init__(self, port = 2231):
        self.port = port
        self.p = process_packet.Pro_pkt()

    def print_port(self):
        print(self.port)

    def listen_from_port(self, sport = 0):
        filter_rule = "udp dst port " + str(self.port) + " and src port " \
                + str(sport)
        return self.p.recv_pkt(filter_rule, 1)

    def get_request_type(self, sport = 0):
        pkt = self.listen_from_port(sport)
        if pkt[0]['Raw'].load == b'read':
            request_type = 'read'
        elif pkt[0]['Raw'].load == b'write':
            request_type = 'write'

        return request_type, pkt[0]['IP']

    def sr1_pkt_from_port(self, request_pkt, dport = 0):
        pkt = request_pkt
        pkt.dport = dport
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()

        re_pkt = self.listen_from_port(dport)
        return re_pkt[0]['IP']

    def send_pkt_to_port(self, send_pkt, dport = 0):
        pkt = send_pkt
        pkt.dport = dport
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()
