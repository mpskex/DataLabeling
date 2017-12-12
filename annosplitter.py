#!/usr/bin/python
# -*- coding:utf-8 -*-
import os


def parse_anno_fromfile(line):
    #   split with space
    t = line.split(" ")
    #   get rid of the return
    a = t[-1].split("\r\n")
    t[-1] = a[0]
    #   name only
    t[0] = t[0].split("/")[-1]
    #   position string to number
    for j in range(10):
        t[j + 1] = int(t[j + 1])
    return t

def parse_anno_tofile(anno):
    #   for single annotation
    t = ""
    t += "frame/"
    t += anno[0]
    #   numbers to string
    for j in range(10):
        t += " "
        t += str(anno[j+1])
    t+="\r\n"
    return t

def cache_anno(annolist):
    for i in annolist:
        t = parse_anno_tofile(i)
        with open("static/anno/"+i[0]+".txt", "w") as f:
            f.write(t)
            f.close()
    return True

def import_anno():
    buff = []
    annodict = {}
    #   open anno list file
    with open("static/pts_list.txt", "r") as f:
        buff = f.readlines()
        f.close()
    #   convert list to dict
    for i in range(len(buff)):
        t = parse_anno_fromfile(buff[i])
        annodict[t[0]] = t
    print len(annodict), " has imported and a type of ", type(annodict), " is returned!"
    return annodict

def anno_out(filename):
    with open(filename, "w") as f:
        f.writelines()
        f.close()

if __name__ == '__main__':
    annolist = import_anno()
    cache_anno(annolist)
