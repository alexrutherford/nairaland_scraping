import csv

inFile=csv.reader(open('post_topics.tsv','r'),delimiter=',')
outFile=csv.writer(open('post_topics_cleaned.tsv','w'),delimiter=',')

for line in inFile:
    print line[0],' '.join(line[1:])
    outFile.writerow([line[0],' '.join(line[1:])])
    if len(line)>2:
        print len(line)
