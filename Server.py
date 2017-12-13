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
names = ['leye', 'reye', 'nose', 'lmth', 'rmth']

#   The level counts that current status of the database
#   if the database is after a whole iteration
#   then level plus one
#   when an record is updated
#   it is appended to next level dict
current_level = 0

#   It is cheaper to random a number
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

@app.route('/submit_imposs', methods=['POST'])
def impossible():
    print 
    print request.form.get('cname')
    print request.form.get('ctext')
    print 
    return redirect(url_for('root'))

@app.route('/confirm', methods=['POST'])
def confirm():
    if request.method == 'POST':
        a = request.form.get('cname').encode('utf-8')
        b = request.form.get('ctext').encode('utf-8')
        buff = b.split(' ')[1:]
        cords = []
        #   if cords length is not 10
        #   or any of it is not able to parse
        for i in buff:
            if not i.isdigit():
                abort(501)
            else:
                cords.append(int(i))
        if len(cords)!=10:
            abort(502)
        #   post data may contain -1
        #   but that is treated like a null position data
        return redirect(url_for('root'))
    abort(501)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/')
def root():
    t1 = time.time()
    r_num = random.randint(0, len(annolist))
    name = annodict[annolist[r_num]][0]
    print "Random number is ", r_num, " Name is ", name
    pname = "static/imgs/" + str(name)
    t2 = time.time()
    print "Quick choose used ", math.floor((t2 - t1)*100000)/100, " ms."
    return render_template('main.html', image = pname, 
            anno=anno2html(annodict[name][1:]))

def anno2html(cords):
    #   convert annotations to svg circles
    _str = ""
    print cords
    for i in range(5):
        #   input the svg point to html
        _str += "<circle cx='"
        _str += str(cords[2*i])
        _str += "' cy='"
        _str += str(cords[2*i+1])
        _str += "' r='2' stroke='"
        #   change its color to identify
        _str += colors[i]
        _str += "' stroke-width='2' fill-opacity='1' filter='Gaussian_Blur'></circle>"
    return _str

@app.errorhandler(401)
def efzo(error):
    return render_template('error.html', resp_code='401', error_message=u'？？？'), 401

@app.errorhandler(501)
def invalid_argument(error):
    return render_template('error.html', resp_code='501', error_message=u'非法输入'), 501

@app.errorhandler(502)
def incomplete_argument(error):
    return render_template('error.html', resp_code='502', error_message=u'不完整输入'), 502

if __name__ == '__main__':
    app.run(debug=True)