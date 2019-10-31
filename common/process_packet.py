#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: process_packet.py
# Created Time: 2019年10月31日 星期四 21时41分51秒
#########################################################################


import os
from scapy.all import Ether
from scapy.all import IP
from scapy.all import UDP
from scapy.all import hexdump
from scapy.all import send
from scapy.all import sniff
from scapy.all import wrpcap
from scapy.all import rdpcap
from scapy.utils import PcapWriter


class Pro_pkt:
    def __init__(self, iface = 'lo', dport = 1111, pkt = None):
        self.iface = iface
        self.dport = dport
        self.pkt = pkt

    def construct_pkt(self, block = None):
        self.pkt = IP()/UDP(sport = 12345, dport = self.dport)/block
        return self.pkt

    def send_pkt(self):
        send(self.pkt, iface = self.iface)

    def recv_pkt(self, filter_rule = None):
        return sniff(iface = self.iface, filter = filter_rule)

    def sr1_pkt(self, filter_rule = None):
        sr1(iface = self.iface, filter = filter_rule)

    def wr_pkt(self, mode = 'node', port = 2234):
        file_name = ''.join([mode, '_', str(port), '.pcap'])
        try:
            pktdump = PcapWriter(file_name, append = True, sync = True)
            pktdump.write(self.pkt)
        except:
            raise Exception

    def rd_one_pkt(self, mode = 'node', port = 2234):
        file_name = ''.join([mode, '_', str(port), '.pcap'])
        try:
            return rdpcap(file_name)[-1]
        except:
            raise Exception

    def rd_all_pkts(self, mode = 'node', port = 2234):
        file_name = ''.join([mode, '_', str(port), '.pcap'])
        try:
            return rdpcap(file_name)
        except:
            raise Exception
