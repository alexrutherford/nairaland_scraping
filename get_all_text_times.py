import glob,sys,re,csv,datetime,traceback
from bs4 import BeautifulSoup
import pymysql
from check_dates import cleanTime

sys.path.append('../ipynb/')

from add_demographics_to_tw_profiles import getQualifyingTaxonomy

from tag_fb_relevant import getTaxonomies 

taxonomyDict=getQualifyingTaxonomy('../ipynb/')

relevantDict=getTaxonomies('../ipynb/')

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur.execute('SET NAMES utf8mb4;')
cur.execute('SET CHARACTER SET utf8mb4;')
cur.execute('SET character_set_connection=utf8mb4;')

v=False

##############
def classifyRelevant(t):
##############
    if re.search(relevantDict['en'],t,re.U) or re.search(relevantDict['ha'],t,re.U):
        return ['1']
    return ['0']
##############
def classifyTopic(t):
##############
    res=[]
    for k in taxonomyDict['en']['topics'].keys():
        if re.search(taxonomyDict['en']['topics'][k],t,re.U) or re.search(taxonomyDict['ha']['topics'][k],t,re.U):
            res.append('1')
        else:
            res.append('0')
    return res
##############
def clean(t):
##############
    t=re.sub(r'\t|\n|\"|\!|\#\.|\?|\;|\:|\,|\(|\)|\<|\>',' ',t.lower(),re.U)
    t=re.sub(r'\'','',t,re.U)
    return t
##############
def getParts(content,fileName,parent):
##############
    t=BeautifulSoup(content)

    res=t.find_all('div',attrs={'class':'narrow'})

    quotes=[r.find_all('blockquote') for r in res]
    # Get all the quotes in the comment (if any exist)

    comments=[r.text for r in res]

    parents=[r.parent for r in res]
    
    parentTexts=[p.text for p in parents]

    parentsLikes=[re.search('[0-9]+ Like',p) for p in parentTexts]
    parentsLikes=[None if not p else p.group().partition(' ')[0] for p in parentsLikes]

    parentsShares=[re.search('[0-9]+ Share',p) for p in parentTexts]
    parentsShares=[None if not p else p.group().partition(' ')[0] for p in parentsShares]
    '''
    if any(parentsShares):
        for n,r in enumerate(zip(parentsShares,parentsLikes)):
            print n,r
    '''
#    print 'likeShares',likesShares

    nComment=0
    comments=[comment[len(quote[0].text):] if len(quote)>0 else comment for comment,quote in zip(comments,quotes)]
    '''Strip quoted comment from the front'''
    comments=[clean(comment) for comment in comments]
    
#    for n,c in enumerate(comments):
#        print n,c

    res2=t.find_all('span',attrs={'class':'s'})
    times=[r.text.decode('utf-8') for r in res2]
    cleanedTimes=[]
    for tempTime in times:
        try:
            cleanedTimes.append(datetime.datetime.strptime(tempTime,'%I:%M%p On %b %d, %Y '))
        except:
            '''parser.parse(time.ctime(os.path.getctime(fileName)) '''
#            print 'Error: ',parent,fileName,'>>'+tempTime+'<<'
#            print traceback.print_exc()
            cleanedTime=cleanTime(tempTime,fileName)
#            print '++++++++GOT CLEANED',cleanedTime
            cleanedTimes.append(cleanedTime)
            '''Some dates don't parse cleanly as date not displayed sometimes'''
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

    return comments,cleanedTimes,users,parentsLikes,parentsShares
##############
def main():
##############

#    postsFile=csv.writer(open('posts.tsv','a'),delimiter='\t')
#    commentsFile=csv.writer(open('comments.tsv','a'),delimiter='\t')
    ''' Write straight to DB here instead of files'''

    outFile=csv.writer(open('LIKES_SHARES.csv','w'),delimiter='\t')

    for parent in range(1798360,2100000):
#    for parent in range(1788360,1788370):
#    for parent in range(2068000,2068100):
        '''108m for 10000'''
        print parent
        parentContent=''
        try:
            parentContent=open('TEXT/'+str(parent)+'.html','r').read()
            children=glob.glob('TEXT/'+str(parent)+'_*html')
            children=[child.partition('_')[2].strip('.html') for child in children]
            children.sort(key=int)
            childNames=[c for c in children]
            children=['TEXT/'+str(parent)+'_'+child+'.html' for child in children]
            # Sort comment pages numerically i.e. 23 after 9
            
            children=[open(child,'r').read() for child in children]
            
            comments,times,users,likes,shares=getParts(parentContent,'TEXT/'+str(parent)+'.html',parent)
            
            if len(comments)==0:
                comments.append('__REMOVED__')
                times.append(datetime.datetime(1970,1,1))
                users.append('__REMOVED__')
                print 'REMOVED?'
                t=BeautifulSoup(parentContent)
                res=t.find_all('h2')
            '''If post removed, no text found, but header shows removal'''

            post,postTime,postUser,postLikes,postShares=comments.pop(0),times.pop(0),users.pop(0),likes.pop(0),shares.pop(0)
#            postsFile.writerow([str(parent),postUser,postTime,post.encode('utf-8')])
            postTime=postTime.strftime('%Y-%m-%d %H:%M:00')
            
            postViews=0
            try:
                postViews=re.search(r'('+r'[0-9]+'+r' Views)',parentContent)
                postViews=str(postViews.group().partition(' ')[0])
                print 'Views',postViews
            except:
                print '::::::::'
                print traceback.print_exc()
                pass

            # Convert datetime to string
            try:
                q=u"insert into posts3 (parent,user,time,content,nLikes,nShares,nViews,relevant,delivery,side_effects,information,advocacy,ideals,efficiency,distrust,safety,news) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                data=[str(parent),postUser,postTime,post.encode('utf-8'),str(postLikes),str(postShares),postViews]+classifyRelevant(post)+classifyTopic(post)
                if True:
                    cur.execute(q,data)
                    cur.connection.commit()
                else:
                    outFile.writerow(['POST',parent,str(postLikes),str(postShares)])
            except:
                'UNICODE ERROR',str(parent)
                print traceback.print_exc()
            assert len(comments)==len(times)==len(users)==len(likes)==len(shares),('Lengths differ',len(comments),len(times),len(users),len(likes),len(shares))

            if v:print '-----\n',post,postTime,postUser,'\n-------\n'

            nComment=0

            for comment,time,user,like,share in zip(comments,times,users,likes,shares):
                if v:print '=>',nComment,comment,time,user
                time=time.strftime('%Y-%m-%d %H:%M:00')
                # Convert datetime to string

                try:
                    q=u"insert into comments3 (parent,nComment,user,time,content,nLikes,nShares) values (%s,%s,%s,%s,%s,%s,%s)"
                    data=(str(parent),str(nComment),user,time,comment.encode('utf-8'),like,share)
                    if True:
                        cur.execute(q,data)
                        cur.connection.commit()
                except:
                    print 'UNICODE ERROR',str(parent),str(nComment)
                    print traceback.print_exc()
                nComment+=1

            for child,childName in zip(children,childNames):
                comments,times,users,likes,shares=getParts(child,'TEXT/'+str(parent)+'_'+childName+'.html',parent)
                assert len(comments)==len(times)==len(users)==len(likes)==len(shares),'Lengths differ'
                
                for comment,time,user,like,share in zip(comments,times,users,likes,shares):
                    if v:print '=>',nComment,comment,time,user,like,share
                    time=time.strftime('%Y-%m-%d %H:%M:00')
                    # Convert datetime to string

                    try:
                        q=u"insert into comments3 (parent,nComment,user,time,content,nLikes,nShares) values (%s,%s,%s,%s,%s,%s,%s)"
                        data=(str(parent),str(nComment),user,time,comment.encode('utf-8'),like,share)
                        if True:
                            cur.execute(q,data)
                            cur.connection.commit()
                    except:
                        print 'UNICODE ERROR',str(parent),str(nComment)
                        print traceback.print_exc()
                    nComment+=1
            parentContent=' '
            print nComment,'comments'
        except:
            print 'MISSING?',parent
            t=BeautifulSoup(parentContent)
            res=t.find_all('h2')
            if len(res)==0:
                print 'YES MISSING'
            else:
#                print ' '.join([r.text for r in res])
                print 'NOT MISSING'
                print traceback.print_exc()
            print '------------------------'
if __name__=="__main__":
    main()
