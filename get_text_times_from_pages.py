# coding: utf-8
import re,sys,os,re,csv,time,glob
import urlparse
from bs4 import BeautifulSoup

########
def getComments(n='1935635'):
########
    try:
        content=open('TEXT/'+n+'.html','r').read()
    except:
        print 'MISSING',n
        return None
    t=BeautifulSoup(content)

    res=t.find_all('div',attrs={'class':'narrow'})

    res2=t.find_all('span',attrs={'class':'s'})

#    print res2[0].text
    '''
    for r in res:
        print r  # comments
    '''

    comments=re.findall(r'/'+n+'/'+'[-a-z0-9]+'+'/'+'[0-9]{1,}',content)
#    comments=re.search(r'/'+n+'/'+'(.*)'+'/'+'[0-9]+',content)
#    comments=re.search(r'/'+n+'/'+'[-a-z0-9]+',content)

#    print n
#    print comments.group()
    return comments
###########
def getCommentsPage(n,c,link):
###########
    link='http://www.nairaland.com/'+'/'.join(link.split('/')[0:-1])
    for cc in c:
    
        print '\t',n,cc,link+'/'+str(cc)
        outName=n+'_'+str(cc)+'.html'
        print outName
        os.system('curl '+link+'/'+str(cc)+' > TEXT/'+outName)

###########
def fillIn(cc):
###########
    print 'filling in',cc
#    stem='/'.join(cc[0].split('/')[0:-1])
    ns=[c.split('/')[-1] for c in cc]
    missing=range(int(ns[-2])+1,int(ns[-1]))
    return list(set(ns+missing))
###########
def main():
###########
    ''' Starts from 1973874 
        ends around 1788360 
        Did 1811873,1913874
        Did 1711873,1811873
        Did 1913874,1973874
    '''
    for n in range(1973874,2020806):
        c=getComments(str(n))
        if c:
            print 'C=>',c
            stem='/'.join(c[0].split('/'))
            c=fillIn(c) # we need this as sometimes hyperlinks only exist to 1,2,3....21
                       
            print n
            print c
            print 'STEM',stem
            print '----------------------'
            getCommentsPage(str(n),c,stem)
if __name__=="__main__":
    main()

