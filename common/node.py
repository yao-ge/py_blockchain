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

    def listen_from_port(self, sport = 0, count = 1):
        #filter_rule = "udp dst port " + str(self.port) + " and src port " \
        #        + str(sport)
        filter_rule = "udp dst port " + str(self.port)
        print(filter_rule)
        print("count:", count)
        return self.p.recv_pkt(filter_rule, count)

    def get_request_type(self, sport = 0):
        pkt = self.listen_from_port(sport)
        if pkt[0]['Raw'].load.startswith(b'read'):
            request_type = 'read'
        elif pkt[0]['Raw'].load.startswith(b'write'):
            request_type = 'write'
        elif pkt[0]['Raw'].load.startswith(b'sync'):
            request_type = 'sync'
        elif pkt[0]['Raw'].load.startswith(b'broadcast'):
            request_type = 'broadcast'
        elif pkt[0]['Raw'].load.startswith(b'exit'):
            request_type = 'exit'

        print(pkt)
        print(pkt.summary())
        return request_type, pkt[0]['IP']

    def change_request_type(self, pkt, old_type, new_type):
        pkt.load = pkt.load.replace(old_type, new_type)
        return pkt

    def sr1_pkt_from_storage_to_node(self, request_pkt, storage_port = 0, node_port = 0):
        pkt = request_pkt
        pkt.dport = storage_port
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()

        re_pkt = self.listen_from_port(storage_port)
        type(re_pkt)
        print(re_pkt)

        self.p.pkt = re_pkt[0]["IP"]
        self.p.pkt.sport = self.port
        self.p.pkt.dport = node_port
        time.sleep(1)
        return self.p.send_pkt()

    def sr1_pkt_from_storage_to_user(self, request_pkt, dport = 0):
        pkt = request_pkt
        pkt.dport = dport
        pkt.sport = self.port
        self.p.pkt = pkt
        self.p.send_pkt()

        re_pkt = self.listen_from_port(dport)
        print("re pkt:")
        print(re_pkt[0])

        pre_header_hash, data_hash, timestamp, nonce = \
                self.pb.unpack_block(re_pkt[0]['IP'].load[:144])

        print(pre_header_hash)
        print(data_hash)
        print(timestamp)
        print(nonce)
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

    def broadcast_to_all_nodes(self, content):
        node_count = self.e.count_cfg("node")
        dport_list = config.nodes_list[0 : node_count]
        self.p.broadcast_pkt(self.port, dport_list, content)
        return node_count

    def gen_pkt_with_pre_header_hash(self, sport = 0, dport = 0, \
            pre_header_hash = '0' * 64):
        pkt = self.p.construct_pkt_with_pre_header_hash(\
                sport, dport, pre_header_hash)
        self.new_header_hash = self.p.new_header_hash
        return pkt

    def send_new_header_hash_to_user(self, sport = 0, dport = 0):
        pkt = self.p.construct_pkt(sport, dport, self.new_header_hash)
        self.p.pkt = pkt
        return self.p.send_pkt()

    def verify_pkt_is_valid(self, pkt):
        block = pkt[0].load
        print("recv block:", block)
        pre_header_hash, data_hash, timestamp, nonce = self.pb.unpack_block(block[:144])
        hash_str = "".join([pre_header_hash.decode(), data_hash.decode(),\
                str(timestamp), str(nonce)])
        self.new_header_hash = self.pb.gen_hash(hash_str)
        self.headers_hash_list.append(self.new_header_hash)
        print("verify hash str:", hash_str, type(hash_str))
        print("verify new header hash:", self.new_header_hash)
        return self.pb.proof_work(hash_str), self.new_header_hash

    def sync_with_other_nodes(self):
        # step1: constuct sync request
        content = 'sync'
        # step2: broadcast request to other nodes
        node_count = self.broadcast_to_all_nodes(content)
        print("broad cast to all nodes, node count:", node_count)
        # step3: recv all pkts from other nodes
        if node_count == 1:
            pkts = self.p.rd_one_pkt(port = self.port)
        else:
            pkts = self.listen_from_port(self.port, node_count - 1)
            print("listen from port, pkts:", pkts.summary())
        # step4: select the maxmun packets and copy files
            #max_block_content = ''
            copy_port = 0
            for pkt in pkts:
                copy_port = copy_port if int(pkt.load.decode()) < copy_port else pkt.sport
                print("copy port:", copy_port)
                #max_block_content = max_block_content if len(pkt.load) < len(max_block_content) else pkt.load
                #print(int(pkt.load.decode()))
                #print("sport:", pkt.sport)
                #print("max block content: ", max_block_content)

            print("port:", self.port)
            #print("max block content:", max_block_content)
            #self.p.construct_pkt(self.port, 3231, max_block_content)
            #self.p.wr_pkt(port = self.port)
            self.p.copy_from_port(copy_port, self.port)
