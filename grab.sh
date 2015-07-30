for(( i=1522047;i<1576341;i++ ))
do
    sleep 0.3
    curl --head "http://www.nairaland.com/$i" >> grabbed.out 
    echo "http://www.nairaland.com/$i" >> grabbed.out
    echo "$i"
done  

