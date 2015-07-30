import os,re,sys,os
import csv,time

inFile=csv.reader(open(sys.argv[1],'r'))

for line in inFile:
    print line[0]
    n=line[0].partition('http://www.nairaland.com/')[2]
    n=n.partition('/')[0]
    print n
    os.system('curl '+line[0]+' > TEXT/'+str(n)+'.html')
    time.sleep(0.2)
