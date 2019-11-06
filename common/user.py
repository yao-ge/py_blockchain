#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: user.py
# Created Time: 2019年10月31日 星期四 17时49分37秒
#########################################################################

from common import process_packet
from common import edit_cfg
from random import randint


class User:
    def __init__(self, port = 1231):
        self.port = port
        self.dport = 2231
        self.pre_header_hash = None
        self.pro_pkt = process_packet.Pro_pkt()
        self.e = edit_cfg.Edit_cfg()

    def print_port(self):
        print(self.port)

    def get_pre_header_hash(self):
        content = "read"
        count = self.e.count_cfg('node')

        #self.dport = 2231 + randint(0, count - 1)
        self.dport = 2231

        self.pro_pkt.construct_pkt(self.port, self.dport, content)
        self.pro_pkt.send_pkt()

        filter_rule = "udp src port " + str(self.dport) + " and dst port " \
                + str(self.port)
        print("recv filter rule in user:{}".format(filter_rule))

        re_pkt = self.pro_pkt.recv_pkt(filter_rule, 1)

        self.pre_header_hash = re_pkt[0]['Raw'].fields['load'][:64] 
        #self.pre_header_hash = re_pkt[0]['Raw'].fields['load'][144:]
        print("pre header hash:{}".format(self.pre_header_hash))
        return self.pre_header_hash

    def read_request(self):
        return self.get_pre_header_hash()

    def write_request(self):
        pass
