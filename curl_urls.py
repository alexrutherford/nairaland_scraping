import os,csv,time

inFile=csv.reader(open('urls.txt','r'),delimiter='\t')

for line in inFile:
    url=line[0]
    os.system('curl '+url+' >> temp.txt')
    os.system('echo "\n+++---\n" >> temp.txt')
    time.sleep(1)
