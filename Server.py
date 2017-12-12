#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import random
import time
import math
import sqlite3
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect

from annosplitter import *

app = Flask(__name__)
annodict = import_anno()
#   make last backup
#os.system("cp -rv static/anno/ static/anno_backup/")
#   make last backup
cache_anno(annodict)

#   annotation point color
colors = ['red', 'blue', 'green', 'yellow', 'pink']

#   The level counts that current status of the database
#   if the database is after a whole iteration
#   then level plus one
#   when an record is updated
#   it is appended to next level dict
current_level = 0

#   This is cheaper to random a number
#   then search it in a hashed dict
#   So this is a quick index of 
#   a hash table of annotation
annolist = []
for i in annodict:
    annolist.append(i)

#   make a multi level queue
#   to get the stuff done
multi_level_queue = {}
multi_level_queue[current_level] = annolist

print "make sure that dict length: ", len(annodict), "is aligned with list lenth: ", len(annolist)

@app.route('/')
def root():
    t1 = time.time()
    r_num = random.randint(0, len(annolist))
    name = annodict[annolist[r_num]][0]
    print "Random number is ", r_num, " Name is ", name
    pname = "static/imgs/" + str(name)
    t2 = time.time()
    print "Quick choose used ", math.floor((t2 - t1)*100000)/100, " ms."
    return render_template('main.html', image = pname, anno=anno2html(name))

def anno2html(name):
    _str = ""
    cords = annodict[name][1:]
    print cords
    for i in range(5):
        _str += "<circle cx='"
        _str += str(cords[2*i])
        _str += "' cy='"
        _str += str(cords[2*i+1])
        _str += "' r='2' stroke='"
        _str += colors[i]
        _str += "' stroke-width='2' fill-opacity='1' filter='Gaussian_Blur'></circle>"
    return _str


if __name__ == '__main__':
    app.run(debug=True)