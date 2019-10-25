#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: construct_block.py
# Created Time: 2019年10月25日 星期五 22时12分25秒
#########################################################################

########## block format #################################################
#   ---------------|--------------
#   pre block hash | 32Bytes
#   ---------------|--------------
#   timestamp      | 4Bytes
#   ---------------|--------------
#   nonce          | 4Bytes
#   ---------------|--------------
#   data           | variable
#   ---------------|--------------
#########################################################################


import struct

def construct_block(pre_head_hash = "0" * 64, timestamp = 0, nonce = 0, \
        data = "0"):
    data_len = len(data)
    print(data_len)
    if 1 == data_len:
        pack_fmt = "".join(['64s', 'i', 'i', 's'])
    else:
        pack_fmt = "".join(['64s', 'i', 'i', str(data_len), 's'])
    print(pack_fmt)
    block = struct.pack(pack_fmt, pre_head_hash.encode('gbk'), timestamp, nonce, data.encode('gbk'))
    return block

