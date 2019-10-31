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


import struct

class Pro_block:
    def __init__(self):
        pass

    def construct_block(self, pre_head_hash = "0" * 64, \
            data_hash = "0" * 64, timestamp = 0, nonce = 0, data = "0"):
        data_len = len(data)
        if 1 == data_len:
            pack_fmt = "".join(['64s', '64s', 'i', 'i', 's'])
        else:
            pack_fmt = "".join(['64s', '64s', 'i', 'i', str(data_len), 's'])
        block = struct.pack(pack_fmt, pre_head_hash.encode('gbk'), \
                data_hash.encode('gbk'), timestamp, nonce, data.encode('gbk'))
        return block
 
