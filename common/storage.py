#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: storage.py
# Created Time: 2019年10月31日 星期四 17时49分37秒
#########################################################################


from common import process_packet

class Storage:
    def __init__(self, port = 3231):
        self.port = port
        self.dport = 0
        self.pkt = None
        self.p = process_packet.Pro_pkt()

    def print_port(self):
        print(self.port)

    def recv_pkt(self):
        filter_rule = "udp dst port " + str(self.port)
        pkt = self.p.recv_pkt(filter_rule, 1)
        self.dport = pkt[0].sport
        self.pkt = pkt[0]['IP']
        return self.pkt

    def get_pkt_from_file(self):
        pkt = self.pkt
        re_pkt = self.p.rd_one_pkt(port = pkt.sport)
        self.pkt = re_pkt
        return re_pkt

    def write_pkt_to_file(self):
        self.p.pkt = self.pkt
        self.p.wr_pkt(port = self.pkt.sport)

    def send_pkt(self):
        pkt = self.pkt
        pkt.sport, pkt.dport = pkt.dport, pkt.sport
        self.p.pkt = pkt
        self.p.send_pkt()

