# -*- coding:utf-8 -*-  
import os


def getData(path):
    file_object = open(path)
    try:
        all_the_text = file_object.readlines()
    finally:
        file_object.close()
    return all_the_text

countD = {}
countD['n'] = 0
path = '../data/features/ncuser-c'
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        print name 
        data = getData(path+'/'+name)
        for i in xrange(0, len(data)):
            line = data[i]
            if line.find('Optional.empty') > -1 :
                countD['n'] += 1
            else:
                a = line.split(',(,Optional[Optional[')
                s = str(a[1])
                # print s[:len(s)-5]
                if not countD.has_key(s[:len(s)-5]):
                    countD[s[:len(s)-5]] = 1
                else: 
                    countD[s[:len(s)-5]] += 1
        
print countD