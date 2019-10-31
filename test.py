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
from common import process_block
from common import edit_cfg
from scapy.all import hexdump


def hash_test():
    data = str(sys.argv[1]).encode('utf-8')
    hash_value = hashlib.sha256(data).hexdigest()
    print("data:\n{} \ndata_hash:\n{}\n".format(data, hash_value))

def gen_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def gen_block():
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
    c = process_block.Pro_block()
    return c.construct_block(pre_block_hash, data_hash, \
            timestamp, nonce, data)

def test_cfg():
    e = edit_cfg.Edit_cfg()
    e.clean_cfg()
    content = {'user': 1234}
    print(content)
    e.wr_cfg(content)
    e.wr_cfg(content)
    data = e.rd_cfg()
    for line in data:
        print(eval(line))
    

def main():
    #hexdump(gen_block())
    test_cfg()


if __name__ == "__main__":
    main()
