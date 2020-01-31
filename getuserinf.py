
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
from gridfs import *


conn = MongoClient('47.105.38.117', 27017)
db2 = conn.userfiledata  # 选定数据库，设定数据库名称为file
fs = GridFS(db2, collection='datas')  # 连接GridFS集合，名称为pdf
for cursor in fs.find():
    filename = cursor.文件名
    content = cursor.read()
    if(not (os.path.exists('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'))):
        os.mkdir('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/')
        if(os.path.exists(not('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename))):
            with open('C:/Users/ENERGY/Desktop/用户数据/' +cursor.来源+'/'+ filename, 'wb') as f:
                f.write(content)