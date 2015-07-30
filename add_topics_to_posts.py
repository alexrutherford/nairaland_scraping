
import pymysql,sys,json
import seaborn as sns
import traceback
import cPickle as pickle
import collections
import numpy as np
import pandas as pd


conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()


# In[4]:

topicDf=pd.read_sql_query('select * from post_topics',conn)


# In[ ]:

for n,row in enumerate(topicDf.iterrows()):
    if n%500==0:
        print n,row[1].parent,row[1].topic
        
    cur.execute("update posts3 set topic='"+row[1].topic+"' where parent='"+row[1].parent+"'")
    conn.commit()


# In[7]:

"update posts3 set topic='"+row[1].topic+"' where parent='"+row[1].parent+"'"


# In[ ]:



