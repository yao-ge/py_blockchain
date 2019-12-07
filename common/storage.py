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

    def recv_pkt(self, sport = 0):
        filter_rule = "udp dst port " + str(self.port) + \
                " and src port " + str(sport)
        pkt = self.p.recv_pkt(filter_rule, 1)
        self.dport = pkt[0].sport
        self.pkt = pkt[0]['IP']
        return self.pkt

    def get_pkt_from_file(self):
        pkt = self.pkt
        re_pkt = self.p.rd_one_pkt(port = pkt.sport)
        self.pkt = re_pkt
        return re_pkt

    def get_all_pkts_from_file(self):
        pkt = self.pkt
        #print("pkt sport:", pkt.sport)
        re_pkt = self.p.rd_all_pkts(port = pkt.sport)
        #print("re pkt:", re_pkt)
        print("get pkts from file:", re_pkt.summary())
        self.pkt = re_pkt.res
        return re_pkt.res

    def write_pkt_to_file(self):
        self.p.pkt = self.pkt
        self.p.wr_pkt(port = self.pkt.sport)

    def send_pkt(self):
        pkts = self.pkt
        if type(pkts) == list:
            for i in range(len(pkts)):
                print(pkts[i].summary())
                pkts[i].sport, pkts[i].dport = pkts[i].dport, pkts[i].sport
                sport, dport = pkts[i].sport, pkts[i].dport
            self.p.construct_pkt(sport, dport, str(len(pkts)))
        else:
            pkts.sport, pkts.dport = pkts.dport, pkts.sport
            sport, dport = pkts.sport, pkts.dport
            self.p.pkt = pkts
        self.p.send_pkt()

