import csv,re

inFile=csv.reader(open('trash.txt','r'),delimiter='\t')
outFile=csv.writer(open('urls.txt','w'),delimiter='\t')
for line in inFile:
    if len(line)>0:
        if re.search('Location',line[0]):
#            print line[0].partition('Location: ')[2]
            outFile.writerow([line[0].partition('Location: ')[2]])
