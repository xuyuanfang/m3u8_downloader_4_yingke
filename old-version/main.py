# -*- coding: utf-8 -*-
"""
Created on 20170113

@author: WHUER
"""

import re
from join import join
import requests
import shutil
import datetime
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')


##############################################################################################################

def get_m3u8_filename(path):
    listfile = os.listdir(path)
    m3u8_filename = ''
    for i in xrange(len(listfile)):
        m3u8_file = re.findall('m3u8', listfile[i])  # "".join(listfile.split())
        if m3u8_file != []:
            m3u8_filename = listfile[i]
    return m3u8_filename

def get_m3u8_info(m3u8_filename):
    m3u8_info = []
    f = open(m3u8_filename)
    lines = f.readlines()
    for line in lines:
        line_info = re.findall('.*?ts', line)
        if line_info != []:
            m3u8_info.append(line_info[0])
    f.close()
    return m3u8_info

def downloader(url, savepath_filename):
    re_data = requests.get(url).content
    output = open(savepath_filename, 'wb')
    output.write(re_data)
    output.close()

##############################################################################################################

path = os.getcwd()
tmp_path = path + '\\ts\\'
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)

m3u8_filename = get_m3u8_filename(path)
try:
    m3u8_info = get_m3u8_info(m3u8_filename)
    m3u8_fileid = re.findall('[0-9]+', m3u8_filename)[0]
except:
    print 'm3u8 file is not found!'
    yingke_url = raw_input("Input yingke_id:") + '='
    scan_m3u8_fileid = re.findall('[0-9]+', yingke_url)
    while scan_m3u8_fileid == []:
        yingke_url = raw_input("Input yingke_id:") + '='
        scan_m3u8_fileid = re.findall('[0-9]+', yingke_url)
    m3u8_fileid = scan_m3u8_fileid[0]
    m3u8_filename = m3u8_fileid + '.m3u8'
    m3u8_url = 'http://record2.inke.cn/record_' + m3u8_fileid + '/' + m3u8_filename
    savepath_filename = path + '\\' + m3u8_filename
    downloader(m3u8_url, savepath_filename)
    m3u8_info = get_m3u8_info(m3u8_filename)

id = re.findall('[0-9]+', m3u8_filename)[0]

m3u8_num = len(m3u8_info)
print 'The all m3u8 slice is ' + str(m3u8_num)
starttime = datetime.datetime.now()

url_ = 'http://record2.inke.cn/record_'
for i in xrange(m3u8_num):
    print 'Downloading and writing ' + m3u8_info[i] + ' ['+ str(i + 1) +'/' + str(m3u8_num) + ']'
    ts_url = url_ + id + '/' + m3u8_info[i]
    savepath_filename = path + '\\ts\\' + m3u8_info[i]
    downloader(ts_url, savepath_filename)
    untilnowtime = datetime.datetime.now()
    interval = (untilnowtime - starttime).seconds
    print 'Saved and past ' + str(interval) + 's'

fromdir = path + '\\ts\\'
tofile = path + '\\' + m3u8_fileid + '.ts'

print 'Combining all files'
join(fromdir, tofile)
print 'Combine successful!'
shutil.rmtree(fromdir)
os.mkdir(fromdir)
print 'Cleaned temp successful!'

endtime = datetime.datetime.now()
interval = (endtime - starttime).seconds
print 'Total time is ' + str(interval/60) + ' min (' + str(interval) + ' s )'