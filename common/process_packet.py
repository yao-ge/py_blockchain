#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: process_packet.py
# Created Time: 2019年10月31日 星期四 21时41分51秒
#########################################################################


import os
from scapy.all import sr1
from scapy.all import IP
from scapy.all import UDP
from scapy.all import hexdump
from scapy.all import send
from scapy.all import sniff
from scapy.all import rdpcap
from scapy.utils import PcapWriter

from common import process_block

dir_prefix = './pcaps/'

class Pro_pkt:
    def __init__(self, iface = 'lo', pkt = None):
        self.iface = iface
        self.pkt = pkt
        self.new_header_hash = '0' * 64
        self.pb = process_block.Pro_block()

    def print_pkt(self, packet):
        print(hexdump(packet))

    def construct_pkt(self, sport = 0, dport = 0, block = None):
        self.pkt = IP()/UDP(sport = sport, dport = dport)/block
        return self.pkt

    def is_file_exists(self, filename, port = 2234):
        if not os.path.exists(filename):
            block = self.pb.create_genesis_block()
            return self.construct_pkt(port, 3231, block)
        else:
            return None

    def construct_pkt_with_pre_header_hash(self, sport, dport, \
            pre_header_hash):
        new_block = self.pb.create_new_block(pre_header_hash)
        self.new_header_hash = self.pb.new_header_hash
        return self.construct_pkt(sport, dport, new_block)

    def send_pkt(self):
        send(self.pkt, iface = self.iface)
        print("send pkt: ", self.pkt.summary())

    def broadcast_pkt(self, sport = 0, dport_list = [], block = None):
        if dport_list:
            self.construct_pkt(sport, dport_list, block)
            self.send_pkt()
        else:
            print("dport list is none\n")

    def recv_pkt(self, filter_rule = None, pkt_count = 1):
        self.pkt = sniff(iface = self.iface, filter = filter_rule, \
                count = pkt_count)
        print("recv pkt: ", self.pkt[0].summary())
        return self.pkt

    def wr_pkt(self, mode = 'node', port = 2234):
        file_name = ''.join([dir_prefix, mode, '_', str(port), '.pcap'])
        try:
            pktdump = PcapWriter(file_name, append = True, sync = True)
            pktdump.write(self.pkt)
        except:
            raise Exception

    def rd_one_pkt(self, mode = 'node', port = 2234):
        file_name = ''.join([dir_prefix, mode, '_', str(port), '.pcap'])
        pkt = self.is_file_exists(file_name, port)
        if pkt:
            self.pkt = pkt
            self.wr_pkt(port = port)
            print("return genesis block")
            return pkt
        try:
            print("return from file")
            return rdpcap(file_name)[-1]
        except:
            raise Exception

    def rd_all_pkts(self, mode = 'node', port = 2234):
        file_name = ''.join([dir_prefix, mode, '_', str(port), '.pcap'])
        try:
            return rdpcap(file_name)
        except:
            raise Exception
