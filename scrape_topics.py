
from bs4 import BeautifulSoup
import urllib,urllib2,re,csv
import pymysql,sys
import glob


def getLocalContent(url):
    with open(url,'r') as inFile:
        content=inFile.read()
    return BeautifulSoup(content)


def getContent(url):
    content=urllib2.urlopen(url).read()
#    content=f.read()
    print 'c:',content
    return BeautifulSoup(content)

files=glob.glob('TEXT/*')
files=[f for f in files if not re.search('_',f)]
# Get rid of all but first pages fr each post

outFile=csv.writer(open('post_topics.tsv','w'))

nMissing=0

for file_ in files:
    index=file_.strip('.html')
    index=index.strip('TEXT/')
    localContent=getLocalContent(file_)
    
    try:
        header=localContent.find_all('h2')[0].text
        if not header=='This topic has been removed or hidden':
            topic=header.split('-')[-2]
            outFile.writerow([index,topic])
        else:
#            print index
            nMissing+=1
    except:
        print 'ERROR PARSING',index
        
print nMissing

