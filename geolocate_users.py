from ungpgeo import Geolocator
import pymysql,sys,collections

sys.path.append('/mnt/home/ubuntu/projects/tools/')
path="/mnt/home/ubuntu/projects/gates/src/geo-data/"

conn = pymysql.connect(host='localhost',user='root',passwd='pulsetini', db='nairaland',charset='utf8')
cur = conn.cursor()

geo = Geolocator.Geolocator()
geo.setFullDetailCountryList(['KE','IN','PK','NG'])
geo.worldAliasFileName = path+"geolocator.aliases"
geo.worldErrorFileName = path+"geolocator.world.errors"
geo.init(dataFileName = path+"ungp-geo.txt.gz", worldPickleFileName = "geo-world-spark.pkl")

'''
0=original string
1=lat
2=long
3=country
4=level
5=division ID
'''

cur.execute("select * from users_new")

nMatches=collections.Counter()
nLevel=collections.Counter()
nCountry=collections.Counter()

users=[r for r in cur]

for res in users:
    loc=geo.geoLocate(res[3])
    if len(loc)>0:
        nMatches[len(loc)]+=1
        nLevel[loc[0][4]]+=1
        nCountry[loc[0][3]]+=1
#        print "update users set country="+loc[0][3]+" where userName='"+res[0]+"'"
        cur.execute("update users_new set country='"+loc[0][3]+"' where userName='"+res[0]+"'")
        cur.connection.commit()
        cur.execute("update users_new set lat="+str(loc[0][1])+" where userName='"+res[0]+"'")
        cur.connection.commit()
        cur.execute("update users_new set lon="+str(loc[0][2])+" where userName='"+res[0]+"'")
        cur.connection.commit()
        cur.execute("update users_new set divisionIndex='"+str(loc[0][5])+"' where userName='"+res[0]+"'")
        cur.connection.commit()

#        print res,loc
#        sys.exit(1)
print 'Matches'
for k,v in nMatches.most_common():
    print k,v

print 'Levels'
for k,v in nLevel.most_common():
    print k,v

print 'Countries'
for k,v in nCountry.most_common():
    print k,v

