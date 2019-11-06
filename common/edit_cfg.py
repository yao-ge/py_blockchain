#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: edit_cfg.py
# Created Time: 2019年10月31日 星期四 23时31分51秒
#########################################################################


class Edit_cfg:
    def __init__(self, file_name = './net_configure.cfg'):
        self.filename = file_name

    def rd_cfg(self):
        with open(self.filename, 'r+') as fd:
            content = fd.readlines()
        return (content)

    def wr_cfg(self, content):
        with open(self.filename, 'a+') as fd:
            fd.writelines(str(content) + '\n')
            fd.flush()

    def clean_cfg(self):
        with open(self.filename, 'w+') as fd:
            fd.truncate()

    def count_cfg(self, content):
        return self.rd_cfg().count(content + "\n")
