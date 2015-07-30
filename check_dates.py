# coding: utf-8
import datetime,time,re
import os.path,sys
from dateutil import parser
import glob
from bs4 import BeautifulSoup

files=glob.glob('TEXT/*html')
##################    
def cleanTime(tTime,f):
##################    
    fileTime=parser.parse(time.ctime(os.path.getctime(f)+(60*60)))
    # Get time file was scraped in local time
#    print '>>>',tTime
    if not re.search(r'201[45]',tTime) and re.search(r'On',tTime):
        if fileTime.month in [1,2,3]:
            missingYear='2015'
        else:
            missingYear='2014'

        return datetime.datetime.strptime(tTime+', '+missingYear,'%I:%M%p On %b %d, %Y')

    if not re.search(r'On',tTime):
#        print '>>'
#        print tTime,'\t',f,'\t',parser.parse(time.ctime(os.path.getctime(f))),'\t',parser.parse(time.ctime(os.path.getctime(f)+(60*60)))#,' | ',time.ctime(os.path.getctime(f)-(60*60*6)),' | ',time.ctime(os.path.getctime(f))
#        print 'Scraping date'
#        print d.year,d.month,d.day
        tempTime=datetime.datetime.strptime(tTime,'%I:%M%p')
# Grab hour and minute from time stamp
        return datetime.datetime(fileTime.year,fileTime.month,fileTime.day,tempTime.hour,tempTime.minute)
# Add in day and month and year from file timstamp 
##################    
def getTimes(f):
##################
    with open(f,'r') as inFile:
        t=BeautifulSoup(inFile.read())
        res2=t.find_all('span',attrs={'class':'s'})
        times=[r.text.decode('utf-8') for r in res2]
        for tTime in times:
            try:
                datetime.datetime.strptime(tTime,'%I:%M%p On %b %d, %Y ')
            except:
                print cleanTime(tTime,f)
               
'''
If no 'On' present, look at month. If November, December; year=>2014
But if month is January, February; year=>2015
'''               
    
##################
def main():
    files.sort()
    for file in files:
        getTimes(file)
if __name__=='__main__':
    main()
