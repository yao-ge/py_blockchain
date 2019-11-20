#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: hash_test.py
# Created Time: 2019年10月31日 星期四 21时02分59秒
#########################################################################


import sys
import time
import random
import hashlib
import multiprocessing
from common import process_block
from scapy.all import hexdump

control_lable = 0

class test_pro:
    def __init__(self):
        pass

    def listen_lable_to_1(self):
        global control_lable
        while True:
            if control_lable == 1:
                break
        print("lable has been set to 1\n")

    def set_lable_to_1(self):
        global control_lable
        time.sleep(5)
        print("before set lable to 1")
        control_lable = 1


def hash_test():
    data = str(sys.argv[1]).encode('utf-8')
    hash_value = hashlib.sha256(data).hexdigest()
    print("data:\n{} \ndata_hash:\n{}\n".format(data, hash_value))

def gen_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def gen_block():
    p = process_block.Pro_block()
    data = "test"
    pre_block_hash = gen_hash("000")
    data_hash = gen_hash(data)
    timestamp = int(time.time())
    nonce = random.randint(0, 65536)
    print("pre block hash:    ", pre_block_hash)
    print("data hash:         ", data_hash)
    print("timestamp:         ", timestamp)
    print("nonce:             ", nonce)
    print("data:              ", data)
    return p.construct_block(pre_block_hash, data_hash, \
            timestamp, nonce, data)

def test_process(data):
    print(data)

def main():
    print("start multiprocess\n")
    t = test_pro()
    p1 = multiprocessing.Process(target = t.listen_lable_to_1, args = ())
    p1.start()
    p2 = multiprocessing.Process(target = t.set_lable_to_1, args = ())
    p2.start()
    p1.join()
    p2.join()
    print("end multiprocess")


if __name__ == "__main__":
    main()
