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

from common import config

genesis_data = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

class Pro_block:
    def __init__(self):
        self.diffculty = config.target_diffculty
        self.new_header_hash = '0' * 64
        pass

    def gen_hash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def is_hash_valid(self, hash_value):
        return hash_value[:self.diffculty] == '0' * self.diffculty

    def proof_work(self, hash_str):
        #print(nonce, self.gen_hash(str(nonce)))
        return self.is_hash_valid(self.gen_hash(hash_str))

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

    def unpack_block(self, block):
        unpack_fmt = "".join(['64s', '64s', 'q', 'q'])
        pre_header_hash, data_hash, timestamp, nonce = struct.unpack(unpack_fmt, \
                block)
        return pre_header_hash, data_hash, timestamp, nonce

    def create_genesis_block(self):
        pre_header_hash = "0" * 64
        data = genesis_data
        data_hash = self.gen_hash(data) 
        timestamp = int(time.time())
        nonce = 0

        hash_str = ''.join([pre_header_hash, data_hash, str(timestamp), str(nonce)])
        self.new_header_hash = self.gen_hash(hash_str)

        return self.construct_block(pre_header_hash, data_hash, timestamp, \
                nonce, data)

    def create_new_block(self, pre_header_hash, data = genesis_data):
        data_hash = self.gen_hash(data)
        timestamp = int(time.time())
        while True:
            nonce = random.randint(0, 4294967295)    # 0xffffffff
            hash_str = ''.join([pre_header_hash, data_hash, str(timestamp), str(nonce)])
            if self.proof_work(hash_str):
                self.new_header_hash = self.gen_hash(hash_str)
                break

        return self.construct_block(pre_header_hash, data_hash, timestamp, \
                nonce, data)
