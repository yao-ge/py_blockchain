#########################################################################
#-*- coding:utf-8 -*-
#!/usr/bin/env python3
# File Name: init_cfg.py
# Created Time: 2019年11月05日 星期二 21时38分32秒
#########################################################################

from common import edit_cfg


def main():
    e = edit_cfg.Edit_cfg()
    e.clean_cfg()


if __name__ == "__main__":
    main()
