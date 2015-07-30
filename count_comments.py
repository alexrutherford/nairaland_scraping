import pymysql,time

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()
cur.execute('select parent,count(*) from comments_2013 group by parent')

for r in cur:
    if r>0:
        print r
        cur2.execute('update posts_2013 set nComments='+str(r[1])+' where parent='+str(r[0]))
        cur2.connection.commit()
