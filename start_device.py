#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: start_device.py
# Created Time: 2019年10月25日 星期五 22时11分05秒
#########################################################################


import os
import sys
import time
import argparse
import multiprocessing
from scapy.all import hexdump

from common import edit_cfg
from common import user, node, storage

#  default port-mode
#  --------|--------
#    1231  |  user
#  --------|--------
#    2231  |  node
#  --------|--------
#    ...   |  ... 
#  --------|--------
#    3231  | storage
#  --------|--------

user_port = 1231
storage_port = 3231

def usage():
    print("\nfile name:", __file__)
    print("USAGE:\n"
          "\tpython ./start_device.py -m [user/node/storage] -p [num]\n")

def print_break():
    print("\n")
    print("#" * 48)
    print("#" * 48)
    print("\n")

def listen_from_other_nodes(target_func, dport, queue):
    pkt = target_func(dport)

def start_user(user_name = 'User', port = user_port):
    pre_header_hash = ''
    new_header_hash = ''
    u = user.User(port)
    while True:
        print_break()
        request_input = input("\n\033[31mread[r]/\033[32mwrite[w]/\033[33mnode join[nj]/\033[34mexit[e]\n\033[37mrequest:")
        if 'r' == request_input or 'read' == request_input:
            pre_header_hash = u.read_request()
            print("pre header hash:", pre_header_hash)
        elif 'w' == request_input or 'write' == request_input:
            new_header_hash = u.write_request()
            print("new header hash:", new_header_hash)
        elif 'e' == request_input or 'exit' == request_input:
            break
        else:
            print("invalid input")
    print("You have start a user: {}[port:{}]".format(user_name, port))

def start_node(node_name = 'Node', port = 2231):
    n = node.Node(port)
    queue = multiprocessing.Queue(2)
    while True:
        print_break()
        print("get request type")
        re_type, re_pkt = n.get_request_type(user_port)
        print(hexdump(re_pkt))
        if 'read' == re_type:
            print("sr1 pkt from port")
            re_pkt = n.sr1_pkt_from_storage_to_user(re_pkt, storage_port)
            print("send pkt to port")
            n.send_new_header_hash_to_user(port, user_port)
        elif 'write' == re_type:
            broad_pkt = n.change_request_type(b"write", b"broadcast")
            n.broadcast_to_all_nodes(pkt)

            #print("pre header hash:", re_pkt.load[5:])
            #re_pkt = n.gen_pkt_with_pre_header_hash(port, storage_port, re_pkt.load[5:].decode())
            #time.sleep(1)
            #n.send_new_header_hash_to_user(port, user_port)
            #print(hexdump(re_pkt))
            #n.send_pkt_to_storage(re_pkt, storage_port)
        elif 'broadcast' == re_type:
            pass
    print("You have start a user: {}[port:{}]".format(node_name, port))

def start_storage(storage_name = 'Storage', port = storage_port):
    s = storage.Storage(port)
    while True:
        print_break()
        re_pkt = s.recv_pkt()
        print("recv pkt: ", hexdump(re_pkt))
        if re_pkt.load.startswith(b'read'):
            print("get pkt from file")
            re_pkt = s.get_pkt_from_file()
            print("send pkt")
            time.sleep(1)
            s.send_pkt()
        else:
            print("write pkt to file")
            s.write_pkt_to_file()
    print("You have start a user: {}[port:{}]".format(storage_name, port))

def parser_args():
    parser = argparse.ArgumentParser(description = "start device")
    parser.add_argument("-m", "--mode", help = "specify the device mode: user/node/storage")
    parser.add_argument("-p", "--port", help = "specify the device port")
    return parser.parse_args()

def main():
    args = parser_args()
    if not args.mode or not args.port:
        usage()

    mode = args.mode.lower()
    port = int(args.port)
    e = edit_cfg.Edit_cfg()
    e.wr_cfg(mode)
    if mode == 'user':
        start_user(args.mode, port)
    elif mode == 'node':
        start_node(args.mode, port)
    elif mode == 'storage':
        start_storage(args.mode, port)

if __name__ == "__main__":
    main()
