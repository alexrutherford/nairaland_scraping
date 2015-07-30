import glob,sys,re,csv,datetime,traceback
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland')
cur = conn.cursor()

v=False

##############
def clean(t):
##############
    t=re.sub(r'\t|\n|\"|\!|\#\.|\?|\;|\:|\,|\(|\)|\<|\>|\/|\\',' ',t.lower(),re.U)
    # .decode('utf-8','replace')
    t=re.sub(r'\'','',t,re.U)
    return t
##############
def getParts(content,fileName,parent):
##############
    t=BeautifulSoup(content,from_encoding="utf-8")

    res=t.find_all('div',attrs={'class':'narrow'})
    
    comments=[clean(r.text) for r in res]
    
    res2=t.find_all('span',attrs={'class':'s'})
    times=[r.text.decode('utf-8') for r in res2]
    cleanedTimes=[]
    for time in times:
        try:
            if not re.search(r'20[0-9]{2,2} ',time):time+=', 2015 '
            cleanedTimes.append(datetime.datetime.strptime(time,'%I:%M%p On %b %d, %Y '))
        except:
            print 'Error: ',parent,fileName,'>>'+time+'<<'
            print traceback.print_exc()
#    times=[datetime.datetime.strptime(time,'%I:%M%p On %b %d, %Y ') for time in times]
    '''10:29am On Aug 04, 2014''' 
    
    res3=t.find_all('a',attrs={'class':'user'})
    users=[r.text for r in res3]

    res4=t.find_all('td',attrs={'class':'bold l pu'})
    missing=[1 if re.search(r'Nobody',r.text) else 0 for r in res4]
    '''Search for missing users'''
    for n,v in enumerate(missing):
        if v==1:
            users.insert(n,'__MISSING__')

    return comments,cleanedTimes,users
##############
def main():
##############

#    postsFile=csv.writer(open('posts.tsv','a'),delimiter='\t')
#    commentsFile=csv.writer(open('comments.tsv','a'),delimiter='\t')
    ''' Write straight to DB here instead of files'''

#    for parent in range(1798361,2068873):
#    for parent in range(1788361,1798361):
    for parent in range(1788361,1789361):
        '''108m for 10000'''
        print parent
        try:
            parentContent=open('TEXT/'+str(parent)+'.html','r').read()
            children=glob.glob('TEXT/'+str(parent)+'_*html')
            children=[child.partition('_')[2].strip('.html') for child in children]
            children.sort(key=int)
            childNames=[c for c in children]
            children=['TEXT/'+str(parent)+'_'+child+'.html' for child in children]
            # Sort comment pages numerically i.e. 23 after 9
            
            children=[open(child,'r').read() for child in children]
            
            comments,times,users=getParts(parentContent,'TEXT/'+str(parent)+'.html',parent)

            post,postTime,postUser=comments.pop(0),times.pop(0),users.pop(0)
#            postsFile.writerow([str(parent),postUser,postTime,post.encode('utf-8')])
            postTime=postTime.strftime('%H:%m %Y-%m-%d')
            # Convert datetime to string
            try:
#                print 'TYPE',type(u"insert into posts (parent,user,time,content) values ('"+str(parent)+"','"+postUser+"','"+postTime+"','"+post.encode('utf-8','ignore')+"')")
                cur.execute(u"insert into posts (parent,user,time,content) values ('"+str(parent)+"','"+postUser+"','"+postTime+"','"+post.encode('utf-8','ignore')+"')")
                cur.connection.commit()
            except:
                'UNICODE ERROR',str(parent)
                print traceback.print_exc()
            assert len(comments)==len(times)==len(users),('Lengths differ',len(comments),len(times),len(users))

            if v:print '-----\n',post,postTime,postUser,'\n-------\n'

            nComment=0

            for comment,time,user in zip(comments,times,users):
                if v:print '=>',nComment,comment,time,user
                time=time.strftime('%H:%m %Y-%m-%d')
                # Convert datetime to string

#                commentsFile.writerow([str(nComment),str(parent),time,user,comment.encode('utf-8')])
##                print comment
##                print type(comment)
                try:
                    cur.execute(u"insert into comments (parent,nComment,user,time,content) values ('"+str(parent)+"','"+str(nComment)+"','"+user+"','"+time+"','"+comment.encode('utf-8','ignore')+"')")
                    cur.connection.commit()
                except:
                    print 'UNICODE ERROR',str(parent),str(nComment)
                    print traceback.print_exc()
                nComment+=1

            for child,childName in zip(children,childNames):
                comments,times,users=getParts(child,childName,parent)
                assert len(comments)==len(times)==len(users),'Lengths differ'
                
                for comment,time,user in zip(comments,times,users):
                    if v:print '=>',nComment,comment,time,user
                    time=time.strftime('%H:%m %Y-%m-%d')
                    # Convert datetime to string

#                    commentsFile.writerow([str(nComment),str(parent),time,user,comment.encode('utf-8')])                
##                    print comment
##                    print type(comment)

                    try:
                        cur.execute(u"insert into comments (parent,nComment,user,time,content) values ('"+str(parent)+"','"+str(nComment)+"','"+user+"','"+time+"','"+comment.encode('utf-8','ignore')+"')")
                        cur.connection.commit()
                    except:
                        print 'UNICODE ERROR',str(parent),str(nComment)
                        print traceback.print_exc()
                    nComment+=1
            parentContent=' '

        except:
            print 'MISSING?',parent
            t=BeautifulSoup(parentContent)
            res=t.find_all('h2')
            if len(res)==0:
                print 'YES MISSING'
            else:
                if v:print ' '.join([r.text for r in res])
                print 'NOT MISSING'
                print traceback.print_exc()
            print '------------------------'

if __name__=="__main__":
    main()
