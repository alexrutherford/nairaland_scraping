import pymysql,sys,json
import seaborn as sns
import traceback
import collections
import pandas as pd

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()


threadStructure={}

postLengths=collections.Counter()

for chosenParent in [str(c) for c in range(1798374,1798374+200000)]:
    print 'n=',chosenParent

    df=pd.read_sql_query('select content,user from comments2 where parent='+chosenParent,conn)
    pdf=pd.read_sql_query('select content,user from posts2 where parent='+chosenParent,conn)

    if pdf.shape[0]>0:
    # Maybe comment is missing
    
        structure=[0]
        try:
            usersSoFar=[pdf.irow(0).user]
        except:
#            print traceback.print_exc()
#            print 'Post author missing',chosenParent
            '''Do something better than omit authoring user?'''
            usersSoFar=[-1]

        for r in df.iterrows():
            try:
                i=usersSoFar.index(r[1].user)
                structure.append(i)
            except:
                usersSoFar.append(r[1].user)
                structure.append(len(usersSoFar)-1)
        threadStructure[chosenParent]=structure
        postLengths[chosenParent]=len(pdf.irow(0).content)


def redundancy(s):
    return len(set(s))/float(len(s))



def propReturning(s):
    '''Proportion of posts by original author'''
    return s.count(s[0])/float(len(s))



threadDf=pd.DataFrame(data={'length':[len(s) for s in threadStructure.values()],
                            'redundancy':[redundancy(s) for s in threadStructure.values()],
                            'returning':[propReturning(s) for s in threadStructure.values()],
                            'postLength':[0.01+postLengths[k] for k in threadStructure.keys()]
                            })


threadDf.head()


threadDf.to_pickle('thread.dat')

