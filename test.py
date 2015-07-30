# -*- coding: utf-8 -*-
import glob,sys,re,csv,datetime,traceback
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland', charset='utf8')
#conn.set_character_set('utf8') // not available in pymysql, probably the same as charset='utf8' in connect, anyways
cur = conn.cursor()
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8mb4;')
cur.execute('SET character_set_connection=utf8mb4;')

def doQue(q, data=None):
  print que
  cur.execute(que, data)
  cur.connection.commit()
  print cur.fetchone()


noUni = u"I am not unicode"
uni = u"мајкеми"

que = u"SELECT \""+noUni+"\" AS dummy FROM DUAL;" # DUAL = dummy table
doQue(que)

try:
  que = u"SELECT \""+uni.encode('utf-8','ignore')+"\" AS dummy FROM DUAL;"
  doQue(que)
except UnicodeDecodeError:
  print "OMG UnicodeDecodeError"

que = u"SELECT %s AS dummy FROM DUAL;"
data = (uni)
doQue(que, data)


#cur.execute(u"insert into posts (parent,user,time,content) values ('"+str(parent)+"','"+postUser+"','"+postTime+"','"+post.encode('utf-8','ignore')+"')")
#cur.connection.commit()
