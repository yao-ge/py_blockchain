#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: process_block.py
# Created Time: 2019年10月25日 星期五 22时12分25秒
#########################################################################

########## block format #################################################
#   ---------------|--------------
#   pre block hash | 32Bytes
#   ---------------|--------------
#   data hash      | 32Bytes
#   ---------------|--------------
#   timestamp      | 4Bytes
#   ---------------|--------------
#   nonce          | 4Bytes
#   ---------------|--------------
#   data           | variable
#   ---------------|--------------
#########################################################################


import time
import struct
import hashlib
import random

genesis_data = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

class Pro_block:
    def __init__(self):
        pass

    def gen_hash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def construct_block(self, pre_head_hash = "0" * 64, \
            data_hash = "0" * 64, timestamp = 0, nonce = 0, data = genesis_data):
        data_len = len(data)
        if 1 == data_len:
            pack_fmt = "".join(['64s', '64s', 'q', 'q', 's'])
        else:
            pack_fmt = "".join(['64s', '64s', 'q', 'q', str(data_len), 's'])
        block = struct.pack(pack_fmt, pre_head_hash.encode('gbk'), \
                data_hash.encode('gbk'), timestamp, nonce, data.encode('gbk'))
        return block

    def create_genesis_block(self):
        pre_header_hash = "0" * 64
        data = genesis_data
        data_hash = self.gen_hash(data) 
        timestamp = int(time.time())
        nonce = random.randint(0, 65536)

        return self.construct_block(pre_header_hash, data_hash, timestamp, \
                nonce, data)

    def create_new_block(self, pre_header_hash, data):
        data_hash = self.gen_hash(data)
        timestamp = int(time.time())
        nonce = random.randint(0, 65536)

        return self.construct_block(pre_header_hash, data_hash, timestamp, \
                nonce, data)
