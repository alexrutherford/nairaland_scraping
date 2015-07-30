import glob,sys,re,csv,datetime,traceback,urllib2,os
from bs4 import BeautifulSoup
import pymysql
import time
import pandas as pd

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()

###########
def userInDB(user):
###########
    res=pd.read_sql_query("select * from users where userName='"+user+"'",conn)
    if res.shape[0]>0:
        return True
    return False
###########
def main():
###########
    '''
    cur2.execute("select distinct user from posts_2013")
#    cur2.execute("select distinct user from comments")
     
    users=[row for row in cur2]
    cur2.close()
    '''
    inFile=csv.reader(open('USERS_updated.csv','r'),delimiter='\t')
    users=[line[0] for line in inFile]
#    print users
#    sys.exit(1)

    nRow=0
    
    for row in users:
        if not row[0] in ['__REMOVED__']:
            user=row.lower()
            print 'USER',user,nRow

            url='http://www.nairaland.com/'+user
            
            if not os.path.exists('PROFILES/profile_'+user+'.html') and not os.path.exists('2013/PROFILES_2013/profile_'+user+'.html'):
                os.system('curl '+url+' >PROFILES/profile_'+user+'.html')

            if not userInDB(row[0]):
#            if True:
                url='PROFILES/profile_'+user+'.html'

                print url
                with open(url,'r') as f:
                    content=f.read()
           
                t=BeautifulSoup(content)
                res=t.find_all('p')
           
                registered=gender=location=personal=lastSeen=timeSpent=posts=other=''
                nPosts=-999

                for r in res:
                    if r.text:
                        if re.search('Time registered',r.text):
                            registered=r.text.partition(':')[2] 
#                            print 'Registered=>',registered
                        elif re.search('Gender',r.text):
                            gender=r.text.partition(':')[2] 
#                            print 'Gender=>',gender
                        elif re.search('Location',r.text):
                            location=r.text.partition(':')[2] 
#                            print 'Location=>',location
                        elif re.search('Personal text',r.text):
                            personal=r.text.partition(':')[2] 
#                            print 'Personal=>',personal
                        elif re.search('Last seen',r.text):
                            lastSeen=r.text.partition(':')[2] 
#                            print 'Last seen=>',lastSeen
                        elif re.search('Time spent online',r.text):
                            timeSpent=r.text.partition(':')[2] 
#                            print 'Time spent=>',timeSpent
                        elif re.search("posts \(|topics \(",r.text):
                            posts=r.text
                            nPosts=re.search('[0-9]+',posts).group(0)
#                            print 'POSTS=>',nPosts
                        else:
                            other=r.text
#                            print '\tOther',other
                        
                q=u'insert into users (userName,registered,gender,location,personal,lastSeen,timeSpent,posts) values (%s,%s,%s,%s,%s,%s,%s,%s)'
                data=[user,registered,gender,location,personal,lastSeen,timeSpent,nPosts]
                cur.execute(q,data)
                cur.connection.commit()

                res=t.find_all('td',attrs={'class':'user'})

                for r in res:
                    parts=r.text.split(',')

#                    print 'FOLLOWING=>',
                    for part in parts:
                        partGender=''
                        if re.search('(m)',part):partGender='m'
                        elif re.search('(f)',part):partGender='f'
                        part=part.strip('()mf')
                        part=part.lstrip()
#                        print part,partGender
                        '''Add to table following source,target'''
                        q=u'insert into following (source,target) values (%s,%s)'
                        data=[user,part]
                        cur.execute(q,data)
                        cur.connection.commit()
#                    print ''

                print '--------------'   
            nRow+=1
            time.sleep(0.5)
            if nRow==999999:   
                print 'EXITING...' 
                sys.exit(1) 


if __name__=="__main__":
    main()
