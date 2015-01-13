import os,re,sys,os
import csv

inFile=csv.reader(open('trash_urls.txt','r'))

for line in inFile:
    print line[0]
    n=line[0].partition('http://www.nairaland.com/')[2]
    n=n.partition('/')[0]
    print n
    os.system('curl '+line[0]+' > TEXT/'+str(n)+'.html')
    sys.exit(1)
