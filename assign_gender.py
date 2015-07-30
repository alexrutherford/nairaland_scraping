import pymysql,time,sys

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()
cur2.execute('select userName,gender from users_new')

userGenderHash={}

for r in cur2:
    userGenderHash[r[0]]=r[1].lstrip()

print 'Got',len(userGenderHash.keys()),'genders'
print userGenderHash.items()[0]

for k,v in userGenderHash.items():
    print "update following_new set targetGender="+v+" where target='"+str(k)+"'"
    cur.execute("update following_new set targetGender='"+v+"' where target='"+str(k)+"'")
    cur.connection.commit()
    cur.execute("update following_new set sourceGender='"+v+"' where source='"+str(k)+"'")
    cur.connection.commit()
    print 'Done'

