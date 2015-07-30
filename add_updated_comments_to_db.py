
# coding: utf-8

# In[1]:

import pymysql,sys
import seaborn as sns
import pandas as pd
from dateutil import parser


# In[7]:

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()


# In[4]:

df=pd.read_sql_query('select * from comments_updated',conn)


# In[5]:

df2=pd.read_sql_query('select * from posts3',conn)


# In[8]:

df3=pd.read_sql_query('select * from comments3',conn)


# ### Take newly scraped comments from comments_updated, test to see if already present in comments to avoid duplicates. Then adjust comment numbering based on how many comments are in DB already

# In[83]:
def isCommentNew(testComment):
#    print testComment
    existingComments=df3[df3['parent']==testComment['parent']]
    matching=existingComments[(existingComments['content']==testComment['content'])&
                 (existingComments['time']==testComment['time'])]
    if matching.shape[0]>0:
        return False
    return True


def addComment(c):
    q=u'insert into comments3 (parent,nComment,user,time,content,relevant,nLikes,nShares,isNew) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cleanedLikes=c.nLikes
    if pd.isnull(cleanedLikes):
        print 'LIKES NULL',cleanedLikes
        cleanedLikes=0
    
    cleanedShares=c.nShares
    if pd.isnull(cleanedShares):
        cleanedShares=0

    data=[c.parent,-1,c.user,c.time.isoformat(),c.content,c.relevant,cleanedLikes,cleanedShares,True]
#    print data
    cur.execute(q,data)
    cur.connection.commit()


# In[82]:

n=0
for c in df.iterrows():
    if isCommentNew(c[1]):
        print 'New comment, adding'
        addComment(c[1])
    if n==100:sys.exit(1)
#    n+=1


# In[53]:

c


# In[54]:

def getCurrentCommentsCount(testComment):
    existingComments=df3[df3['parent']==testComment['parent']]
    return existingComments.shape[0]


# In[57]:

c[1]['parent']


# In[58]:

getCurrentCommentsCount(c[1])


# In[47]:

isCommentNew(df.iloc[1])


# In[15]:

testComment=df.head(1)


# In[16]:

testComment


# In[18]:

existingComments=df3[df3['parent']==testComment['parent'].values[0]]


# In[23]:

matching=existingComments[(existingComments['content']==testComment['content'].values[0])&
                 (existingComments['time']==testComment['time'].values[0])]


# In[24]:

matching.shape


# In[48]:


# In[ ]:



