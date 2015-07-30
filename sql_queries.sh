select a.source,a.target,b.gender sourceGender,c.gender targetGender from following a inner join users b on a.source=b.userName inner join users c on a.target=c.userName limit 10;
# Get gender of following links

alter ignore table users_new_test add unique index i (userName);
#Remove rows with duplicate userName field

mysqldump -u root -p nairaland > 2015_05_15_nairaland_bakup.sql
# Backup
