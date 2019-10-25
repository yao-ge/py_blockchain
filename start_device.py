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


def start_user(user_name = 'User', port = 1234):
    print("You have start a user: {}[port:{}]".format(user_name, port))

def start_node(node_name = 'Node', port = 2234):
    print("You have start a user: {}[port:{}]".format(node_name, port))

def start_storage(storage_name = 'Storage', port = 3234):
    print("You have start a user: {}[port:{}]".format(storage_name, port))

def parser_args():
    parser = argparse.ArgumentParser(description = "start device")
    parser.add_argument("-m", "--mode", help = "specify the device mode: user/node/storage")
    parser.add_argument("-p", "--port", help = "specify the device port")
    return parser.parse_args()

def main():
    args = parser_args()
    if args.mode:
        print(args.mode)
    #start_user()
    #start_node()
    #start_storage()
    time.sleep(5)

if __name__ == "__main__":
    main()
