#coding=utf-8
'''
Created on 2017年4月10日

@author: gb
'''
from pyquery import PyQuery as pyq 
import urllib2 
import BitVector  
import os  
import sys  
import time
  
class SimpleHash():
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed
    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        return (self.cap-1) & ret   
  
class BloomFilter():
    def __init__(self, BIT_SIZE=1<<25):
        self.BIT_SIZE = 1 << 25
        self.seeds = [5, 7, 11, 13, 17, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []
          
        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))
          
    def insert(self, value):
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1
    def isContaions(self, value):
        if value == None:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            ret = ret & self.bitset[loc]
        return ret




bloomfilter = BloomFilter()
# typeList = [(101,112),(102,105),(109,102),(110,106),(111,113),(103,111),(104,105),(105,120)]
typeList = [(101,115)]
out = open('bd1.txt','w')
count = 0;
while True:
    for typeT in typeList:
        begin = 115000+typeT[0]
        end = 115000+typeT[1]
        while begin <= end:
            url = 'https://zhidao.baidu.com/list?cid='+str(begin)
            html = urllib2.urlopen(url).read()
            jq = pyq(html)
            # print jq('title')            # 获取 title 标签的源码
            # # <title>这是标题</title>
            question_title =  jq('.title-link')    # 获取 title 标签的内容
            # # 这是标题
            # print jq('#hi').text()       # 获取 id 为 hi 的标签的内容
            # # Hello
            #  
            # li = jq('li')                # 处理多个元素
            for i in question_title:
                txt =  pyq(i).text()
                if len(txt)>7:
                    if bloomfilter.isContaions(txt) == False:  
                        bloomfilter.insert(txt)
                        out.write(txt.encode("utf-8"))
                        out.write("\r\n")
                        print txt,count
                        count = count + 1
            begin = begin + 1
    time.sleep(2)
out.close()
