#!/usr/bin/ python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2021/06/14 21:21:27
@Author  :   Enbo Yang
@Version :   0.1
@Contact :   enboyang@outlook.com
@License :   GPL v3
@Desc    :   Copyright (c) 2021 Enbo Yang
'''

# here put the import lib
import configparser


def readcfg(filename):
    cfg = configparser.ConfigParser()
    cfg.read(filename, encoding='utf-8')

    return cfg


if __name__ == '__main__':
    pass
