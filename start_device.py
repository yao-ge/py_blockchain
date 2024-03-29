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
    print("#" * 48)
    print("#" * 48)
    print("\n")

def listen_from_other_nodes(node, dport, queue, lock):
    while True:
        # step1: recv pkt from other nodes
        #print("step1: recv pkt from other nodes\n")
        pkt = node.listen_from_port()
        #lock.acquire()
        #print("before put is recvd pkt:", is_recvd_pkt)
        #queue.get()
        #queue.put(1)
        # step2: verify the pkt
        #print("step2: verify the pkt\n")
        re_value, new_header_hash = node.verify_pkt_is_valid(pkt)
        # step3: set queue to 1 indicates recvd pkt
        #print("step3: set queue to 1 indicates recvd pkt\n")
        #print("re value:", re_value)
        if re_value == True:
            print("send pkt to storage")
            node.send_pkt_to_storage(pkt[0]["IP"], storage_port)
            break
        else:
            continue
        #lock.release()
        # step4: send pkt to storage

def do_proof_work_job(pre_header_hash, node, sport, queue, lock):
    # step1: do proof work job
    #print("step1: do proof work job\n")
    pkt = node.gen_pkt_with_pre_header_hash(sport, storage_port, pre_header_hash)
    # step2: determine the queue
    #print("step2: determine the queue\n")
    #is_recvd_pkt = queue.get()
    # step3: send new pkt to other nodes and storage
    #if is_recvd_pkt == 1:
    #    is_recvd_pkt = 0
    #    queue.put(is_recvd_pkt)
    #    pass
    #else:
    time.sleep(1)
    #lock.acquire()
    #print("step3: send new pkt to other nodes and user\n")
    #if queue.get() == 0:
    if 1:
        node.broadcast_to_all_nodes(pkt[0].load)
        node.send_new_header_hash_to_user(sport, user_port)
        #print("after send is recvd pkt:", is_recvd_pkt)
    else:
        print("queue is 0")
    #queue.put(0)
    #lock.release()
    # step4: send new header hash to user


def start_user(user_name = 'User', port = user_port):
    pre_header_hash = ''
    new_header_hash = ''
    u = user.User(port)
    while True:
        print_break()
        request_input = input("\n\033[31mread[r]/\033[32mwrite[w]/\033[34mexit[e]\n\033[37mrequest:")
        if 'r' == request_input or 'read' == request_input:
            pre_header_hash = u.read_request()
            print("pre header hash:", pre_header_hash)
        elif 'w' == request_input or 'write' == request_input:
            new_header_hash = u.write_request()
            print("new header hash:", new_header_hash)
        elif 'e' == request_input or 'exit' == request_input:
            u.exit_request()
            break
        else:
            print("invalid input")
    print("You have start a user: {}[port:{}]".format(user_name, port))

def start_node(node_name = 'Node', port = 2231):
    n = node.Node(port)
    queue = multiprocessing.Queue(1)
    queue.put(0)
    lock = multiprocessing.Lock()
    n.sync_with_other_nodes()
    while True:
        print_break()
        print("get request type")
        re_type, re_pkt = n.get_request_type(user_port)
        (hexdump(re_pkt))
        if 'read' == re_type:
            #print("sr1 pkt from port")
            re_pkt = n.sr1_pkt_from_storage_to_user(re_pkt, storage_port)
            #print("send pkt to port")
            n.send_new_header_hash_to_user(port, user_port)
        elif 'write' == re_type:
            broad_pkt = n.change_request_type(re_pkt, b"write", b"broadcast")
            n.broadcast_to_all_nodes(broad_pkt.load)

            #print("start child process in write mode")
            p1 = multiprocessing.Process(target = listen_from_other_nodes, \
                    args = (n, port, queue, lock))
            p1.start()
            
            p2 = multiprocessing.Process(target = do_proof_work_job, \
                    args = (re_pkt.load[9:].decode(), n, port, queue, lock))
            p2.start()
            p1.join()
            p2.join()

            #print("pre header hash:", re_pkt.load[5:])
            #re_pkt = n.gen_pkt_with_pre_header_hash(port, storage_port, re_pkt.load[5:].decode())
            #time.sleep(1)
            #n.send_new_header_hash_to_user(port, user_port)
            #print(hexdump(re_pkt))
            #n.send_pkt_to_storage(re_pkt, storage_port)
        elif 'broadcast' == re_type:
            #print("start child process in broadcast mode")
            p1 = multiprocessing.Process(target = listen_from_other_nodes, \
                    args = (n, port, queue, lock))
            p1.start()
            
            p2 = multiprocessing.Process(target = do_proof_work_job, \
                    args = (re_pkt.load[9:].decode(), n, port, queue, lock))
            p2.start()
            p1.join()
            p2.join()
        elif 'sync' == re_type:
            target_node_port = re_pkt.sport
            #print("recv sync request, target port:", target_node_port)
            n.sr1_pkt_from_storage_to_node(re_pkt, storage_port, target_node_port)
        elif 'exit' == re_type:
            n.broadcast_to_all_nodes(re_pkt.load)
            n.send_pkt_to_storage(re_pkt, storage_port)
            break;
    print("You have start a user: {}[port:{}]".format(node_name, port))

def start_storage(storage_name = 'Storage', port = storage_port, listen_port = 0, lock = None):
    s = storage.Storage(port)
    while True:
        print_break()
        re_pkt = s.recv_pkt(listen_port)
        lock.acquire()
        (hexdump(re_pkt))
        if re_pkt.load.startswith(b'read'):
            print("get pkt from file")
            re_pkt = s.get_pkt_from_file()
            print("send pkt")
            time.sleep(1)
            s.send_pkt()
        elif re_pkt.load.startswith(b'exit'):
            lock.release()
            break
        elif re_pkt.load.startswith(b'sync'):
            re_pkt = s.get_all_pkts_from_file()
            time.sleep(1)
            s.send_pkt()
        else:
            print("write pkt to file")
            s.write_pkt_to_file()
        lock.release()
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
        lock = multiprocessing.Lock()
        p1 = multiprocessing.Process(target = start_storage, args = (args.mode, port, 2231, lock))
        p1.start()
        p2 = multiprocessing.Process(target = start_storage, args = (args.mode, port, 2232, lock))
        p2.start()
        #p3 = multiprocessing.Process(target = start_storage, args = (args.mode, port, 2233, lock))
        #p3.start()
        #p4 = multiprocessing.Process(target = start_storage, args = (args.mode, port, 2234, lock))
        #p4.start()
        #p5 = multiprocessing.Process(target = start_storage, args = (args.mode, port, 2235, lock))
        #p5.start()
        p1.join()
        p2.join()
        #p3.join()
        #p4.join()
        #p5.join()
        #start_storage(args.mode, port)

if __name__ == "__main__":
    main()
