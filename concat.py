#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import re

def concat(filename, path):
    with open(filename, 'w') as f:
        for fn in os.listdir(path):
            if fn.split('.')[-1] == "txt":
                fp = os.path.join(path, fn)
                if not os.path.isdir(fp):
                    with open(fp, 'r') as fsrc:
                        f.write(fsrc.readlines()[0])

if __name__ == '__main__':
    concat("result.txt", "static/anno")