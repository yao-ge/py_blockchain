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

from common import edit_cfg
from common import user, node, storage

def usage():
    print("\nfile name:", __file__)
    print("USAGE:\n"
          "\tpython ./start_device.py -m [user/node/storage] -p [num]\n")

def start_user(user_name = 'User', port = 1234):
    pre_header_hash = ''
    u = user.User()
    while True:
        request_input = input("\nread[r]/write[w]/exit[e]\nrequest:")
        if 'r' == request_input or 'read' == request_input:
            pre_header_hash = u.read_request()
            print("this is a read request")
        elif 'w' == request_input or 'write' == request_input:
            print("this is a write request")
        elif 'e' == request_input or 'exit' == request_input:
            break
        else:
            print("invalid input")
    print("You have start a user: {}[port:{}]".format(user_name, port))

def start_node(node_name = 'Node', port = 2234):
    n = node.Node()
    while True:
        print("get request type")
        re_type, re_pkt = n.get_request_type(1231)
        print(re_type, re_pkt)
        print("sr1 pkt from port")
        re_pkt = n.sr1_pkt_from_port(re_pkt, 3231)
        print("send pkt to port")
        n.send_pkt_to_port(re_pkt, 1231)
    print("You have start a user: {}[port:{}]".format(node_name, port))

def start_storage(storage_name = 'Storage', port = 3234):
    s = storage.Storage()
    while True:
        print("recv pkt")
        re_pkt = s.recv_pkt()
        print(re_pkt)
        print("write pkt to file")
        #s.write_pkt_to_file()
        print("get pkt from file")
        re_pkt = s.get_pkt_from_file()
        print("send pkt")
        time.sleep(0.5)
        s.send_pkt()
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
    e = edit_cfg.Edit_cfg()
    e.wr_cfg(mode)
    if mode == 'user':
        start_user(args.mode, args.port)
    elif mode == 'node':
        start_node(args.mode, args.port)
    elif mode == 'storage':
        start_storage(args.mode, args.port)


if __name__ == "__main__":
    main()
