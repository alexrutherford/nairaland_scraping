import pymysql,sys,json,csv,os,glob,re,time
import collections,datetime
from dateutil import parser
import subprocess
import pandas as pd

from get_all_text_times import getParts

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()

df=pd.read_sql_query("select parent,nComments from posts3 where not content like '%REMOVED%' and parent>1805863",conn)

allCommentsDf=pd.read_sql_query("select parent,user,time from comments3",conn)

#df=pd.read_sql_query("select parent,nComments from posts3 where not content like '%REMOVED%' and parent=1895874",conn)

url='http://www.nairaland.com/'

nRunningCount=0

##############
def curlFile(n,nPage=1):
##############
    print 'CURLING',n,nPage
    if nPage==1:
        finalUrl=getFinalUrl(n)
        if finalUrl:
            o=os.system('curl "'+finalUrl+'" >TEXT_UPDATE/'+str(n)+'.html')
        else:
            print 'Returning None'
            return None
    else:
        finalUrl=getFinalUrl(n,nPage=nPage)
        if finalUrl:
            o=os.system('curl "'+finalUrl+'" >TEXT_UPDATE/'+str(n)+'_'+str(nPage-1)+'.html')
        else:
            print 'Returning None'
            return None
##############
def getFinalUrl(n,v=False,nPage=1):
##############
    p=subprocess.Popen('curl --head "http://www.nairaland.com/'+str(n)+'"',stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    o=p.communicate()

    
    for line in o[0].split('\r\n'):
        if re.search('Location: ',line):
            print '=====================',line
            if nPage==1:
                return line.split(' ')[1]
            elif line.split('/')[-1].isdigit():
                return line.split(' ')[1]+'/'+str(nPage-1)
    print '!!!!COULDNT GREP URL'
    return None
##############
def getCommentFiles(n):
##############
    files=glob.glob('TEXT/'+str(n)+'*')
    if len(files)==0:
        print '!!!!!NO FILES'
    return files

##############
def checkForNewComments(n=1798372):
##############
    '''Opens previously grabbed file and returns parts'''
    parentContent=open('TEXT_UPDATE/'+str(n)+'.html').read()
    comments,times,users,likes,shares=getParts(parentContent,'TEXT_UPDATE/'+str(n)+'.html',n)

##############
def isLastCommentRecent(n,lastTime,dayTolerance=7,v=False,nPage=1):
##############
    '''Check timestamp of last activity on thread against timestamp of file creation
    If within a certain tolerance, returns bool'''
    if nPage==1:
        t=os.path.getctime('TEXT/'+str(n)+'.html')
    else:
        t=os.path.getctime('TEXT/'+str(n)+'_'+str(nPage-1)+'.html')
    
    t=parser.parse(time.ctime(t))
    if v:
        print t,' - ',lastTime
    if (t-lastTime).days<dayTolerance:
        return True
    else:
        return False

##############
def isFileMissing(n,v=False,nPage=1):
##############
    if nPage==1:
        returnVal=os.path.exists('TEXT_UPDATE/'+str(n)+'.html')
    else:
        returnVal=os.path.exists('TEXT_UPDATE/'+str(n)+'_'+str(nPage-1)+'.html')
    if returnVal:
        print 'GOT IT'
        return False
    else:
        print 'NEED IT'
        return True

##############
def putInDb(comments,times,users,likes,shares,flipped,firstPage,n):
##############

    global nRunningCount

    resShape=0
    v=True
    nComment=0
    print 'QUERYING FOR',n
    res=pd.read_sql_query("select * from comments3 where parent='"+str(n)+"'",conn)
    nComment=res.shape[0]
    # Get number of comments so far
    
    try:
        post,postTime,postUser,postLikes,postShares=comments.pop(0),times.pop(0),users.pop(0),likes.pop(0),shares.pop(0)
        # We don't need the post, only interested in comments
    except:
        return
    # If it is empty then do nothing
    print 'GOING INTO LOOP' 
    for comment,time_,user,like,share in zip(comments,times,users,likes,shares):
        #print '=>',nRunningCount,comment,time,user
        postTime=time_.strftime('%Y-%m-%d %H:%M:00')
        # Convert datetime to string

#        res=cur.execute("select * from comments3 where parent='"+str(n)+"' and user='"+user+"' and time='"+postTime+"'")
#        print '+++',res,"select * from comments3 where parent='"+str(n)+"' and user='"+user+"' and time='"+postTime+"'"
        if not flipped:
#            res=pd.read_sql_query("select * from comments3 where parent='"+str(n)+"' and user='"+user+"' and time='"+postTime+"'",conn)
            res=allCommentsDf[(allCommentsDf.parent==str(n))&(allCommentsDf.user==user)&(allCommentsDf.time==postTime)]
            #

#
            resShape=res.shape[0]
        else:
            resShape=0
        # TODO make a bool, flip it once a missing comment is found
        # then saves time checking for each comment
    
        if resShape==0:
            flipped=True

#            print '\t\tINSERTING',nComment,postTime#,comment
            q=u"insert into comments_updated (parent,nComment,user,time,content,nLikes,nShares) values (%s,%s,%s,%s,%s,%s,%s)"
            '''datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00') '''
            data=(str(n),str(nRunningCount),user,postTime,comment.encode('utf-8'),like,share)
            if True:
                cur.execute(q,data)
                cur.connection.commit()
                
                q=u'update posts3 set updated= %s where parent=%s'
                data=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00'),str(n))
                cur.execute(q,data)
                cur.connection.commit()
        else:
            print '\t\tALREADY GOT IT'
        nRunningCount+=1
    return flipped

##############
def getNewComments(n,nCommentsPages):
##############
    
    flipped=False
    # Test to see if the first comments are in the DB
    # Once one comment is found that is missing, put
    # all others in DB without testing
   
    success=True
    # Flag for catching when we cannot curl pages
   
    comments=[]
   
   
    print '+++++++++',n,nCommentsPages
    
    if nCommentsPages==1:
        '''If only a single page just grab first page'''
        if isFileMissing(n,nPage=nCommentsPages):
            success=curlFile(n,nPage=nCommentsPages)

        if success:
            parentContent=open('TEXT_UPDATE/'+str(n)+'.html').read()
            comments,times,users,likes,shares=getParts(parentContent,'TEXT_UPDATE/'+str(n)+'.html',n)
    else:
        '''Otherwise grab the last page'''
        if isFileMissing(n,nPage=nCommentsPages):
            success=curlFile(n,nPage=nCommentsPages)

        if success:
            parentContent=open('TEXT_UPDATE/'+str(n)+'_'+str(nCommentsPages-1)+'.html').read()
            comments,times,users,likes,shares=getParts(parentContent,'TEXT_UPDATE/'+str(n)+'_'+str(nCommentsPages-1)+'.html',n)
            print '\t',len(comments),'COMMENTS FOR PAGE #',nCommentsPages
        
    print 'SUCCESS',success
    if success:
        flipped=putInDb(comments,times,users,likes,shares,flipped,firstPage=True,n=n)
        
    while len(comments)>0:
        nCommentsPages+=1
        comments=[]
        if isFileMissing(n,nPage=nCommentsPages):
            success=curlFile(n,nPage=nCommentsPages)
            print '=======',nCommentsPages,success
        if success:
            parentContent=open('TEXT_UPDATE/'+str(n)+'_'+str(nCommentsPages-1)+'.html').read()
            comments,times,users,likes,shares=getParts(parentContent,'TEXT_UPDATE/'+str(n)+'_'+str(nCommentsPages-1)+'.html',n)
            print '\t',len(comments),'COMMENTS FOR PAGE #',nCommentsPages

        if success:
            flipped=putInDb(comments,times,users,likes,shares,flipped,firstPage=False,n=n)

#############
def main():
#############
    global nRunningCount
    nRow=0

    for row in df.iterrows():
        n=row[1].parent
        nRunningCount=0

        nCommentsPages=len(getCommentFiles(n))
        
        if isFileMissing(n,nPage=nCommentsPages):
            curlFile(n,nPage=nCommentsPages)
        # Automatically grab the first page for every single thread
        # Decide after if we want to grab later pages
            
        print row[0],n,row[1].nComments,' - ',nCommentsPages
        
        if nCommentsPages==1:
            '''If only a single page just grab first page'''
            parentContent=open('TEXT/'+str(n)+'.html').read()
            comments,times,users,likes,shares=getParts(parentContent,'TEXT/'+str(n)+'.html',n)
        else:
            '''Otherwise grab the last page'''
            parentContent=open('TEXT/'+str(n)+'_'+str(nCommentsPages-1)+'.html').read()
            comments,times,users,likes,shares=getParts(parentContent,'TEXT/'+str(n)+'_'+str(nCommentsPages-1)+'.html',n)
            
#    if isLastCommentRecent(n,times[-1],v=True):
        if True:
            curlFile(n,nPage=nCommentsPages)
            getNewComments(n,nCommentsPages=nCommentsPages)

            
#        print isLastCommentRecent(n,times[-1],v=True)
        print '---------------------'
        # If recent, check to see if the comments from the last page should be put in DB
        # Then count pages of comments present from the base page
        nRow+=1
if __name__=='__main__':
    main()
