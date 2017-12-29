#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import random
import time
import math
import sqlite3
from flask import Flask, request, url_for, render_template, make_response
from flask import abort, redirect

from annosplitter import *
from concat import *

app = Flask(__name__)
annodict = import_anno()
#   make last backup
#os.system("cp -rv static/anno/ static/anno_backup/")
#   make last backup
cache_anno(annodict)

def loadprog(filename):
    """
        load the progress file
    """
    annoli = []
    with open(filename, 'r') as f:
        buff = f.readlines()
        f.close()
    for i in range(len(buff)):
        annoli.append(buff[i].split("\r\n")[0])
    return annoli


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
#   backup progress file
annolist = []
progbak = "annotation.prog"
if os.path.exists(progbak):
    annolist = loadprog(progbak)
    count = len(annodict) - len(annolist)
else:
    #   count the annotated pics
    count = 0
    for i in annodict:
        annolist.append(i)
print len(annolist), " remains... and ", len(annodict), " in annodict"
#   working files
working_files = []

#   make a multi level queue
#   to get the stuff done
multi_level_queue = {}
multi_level_queue[current_level] = annolist

print "make sure that dict length: ", len(annodict), "is aligned with list lenth: ", len(annolist)

@app.route('/submit_imposs', methods=['POST'])
def impossible():
    global current_level
    global count
    if request.method == 'POST':
        a = request.form.get('iname').encode('utf-8')
        #   get name
        name = a.split('/')[-1]
        with open("static/impossible.txt", "a") as f:
            f.write(name)
            f.write("\r\n")
            f.close()
        #   remove it from current level queue
        multi_level_queue[current_level].remove(name)
        print "current queue length is ", len(multi_level_queue[current_level])
        #   plus count
        count += 1
        #   remove from dict
        annodict.pop(name)
    return redirect(url_for('root'))

@app.route('/monitor')
def monitor():
    return render_template('monitor.html', percentage="%.2f"%((len(annodict)-float(len(annolist)))/len(annodict)),count=count)

@app.route('/confirm', methods=['POST'])
def confirm():
    global current_level
    global count
    if request.method == 'POST':
        t1 = time.time()
        a = request.form.get('cname').encode('utf-8')
        b = request.form.get('ctext').encode('utf-8')
        buff = b.split(' ')
        cords = []
        #   if cords length is not 10
        #   or any of it is not able to parse
        for i in buff:
            if i=='':
                buff.remove(i)
                continue
            elif not re.match(r'^-?(\.\d+|\d+(\.\d+)?)', i):
                abort(501)
        for i in buff:
            cords.append(int(i))
        if len(cords)!=10:
            abort(502)
        #   get name
        name = a.split('/')[-1]
        #   if anyone else is using this
        if name in working_files:
            abort(503)
        #   then add it to working list
        working_files.append(name)
        print "working static/anno/"+ name +".txt..."

        #   build annotation
        anno = cords
        anno.insert(0, name)
        #   read the origin annotation
        ori_anno = []
        with open("static/anno/"+ name +".txt", "r") as f:
            line = f.readlines()
            ori_anno = parse_anno_fromstring(line[0])
            f.close()
        #   post data may contain -1
        #   but that is treated like a null position data
        #   if the input value is -1 then remain its origin
        for i in range(10):
            if anno[i+1] == -1:
                anno[i+1] = ori_anno[i+1]
        #   write the annotation to file
        with open("static/anno/"+ name +".txt", "w") as f:
            annostr = parse_anno_tostring(anno)
            print annostr
            f.write(annostr)
            f.close()
        
        #   remove it from current level queue
        multi_level_queue[current_level].remove(name)
        print "current queue length is ", len(multi_level_queue[current_level])

        #   if the queue is after one iteration
        #   then plus it to next
        if len(multi_level_queue[current_level]) == 0:
            current_level += 1
            count = 0
        count += 1
        
        #   save progress
        saveprog(progbak, multi_level_queue[current_level])
        if count%100==0:
            saveprog(progbak+'-'+str(float(count)/1000)+'k', multi_level_queue[current_level])
        #   write to pts list
        if count%100==0:
            concat("static/pts_list.txt", "static/anno")
        #   release the working lock
        working_files.remove(name)

        t2 = time.time()
        print "cost ", math.floor((t2 - t1)*100000)/100, " ms."
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


def saveprog(filename, annoli):
    """
        save the progress file
    """
    with open(filename, 'w') as f:
        for i in annoli:
            f.write(i)
            f.write("\r\n")
        f.close()
    return True

def anno2html(cords):
    #   convert annotations to svg circles
    _str = ""
    print cords
    for i in range(5):
        #   input the svg point to html
        _str += "<circle id='svg_"
        _str += names[i]
        _str += "' cx='"
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

@app.errorhandler(503)
def incomplete_argument(error):
    return render_template('error.html', resp_code='503', error_message=u'该资源正忙'), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=80)
