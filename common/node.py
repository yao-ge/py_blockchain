#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: node.py
# Created Time: 2019年10月31日 星期四 17时49分37秒
#########################################################################


class Node:
    def __init__(self, port = 1234):
        self.port = port

    def print_port(self):
        print(self.port)
