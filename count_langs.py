import pymysql,time
import langid,collections

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()
cur2 = conn.cursor()
cur2.execute('select content from posts')

langCounter=collections.Counter()
vals=[]
lengths=[]
probs=[]

def clean(s):
    s=re.sub(r'\?|\.|\,|\:|\;|\"|\&|\@|\!|\*|\=|\+|\-|\_|\n|\t|\/|\\',' ',s.lower())
    return s.split()

for r in cur2:
    l=langid.classify(r[0])
    langCounter[l[0]]+=1
    vals.append(l[1])
    lengths.append(len(r[0]))

print langCounter.most_common(10)
