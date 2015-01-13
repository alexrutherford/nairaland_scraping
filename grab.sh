for((i=1785400;i>1757360;i--)); 
# 1788360
do
    sleep 1
    curl --head 'http://www.nairaland.com/'$i  
    echo 'http://www.nairaland.com/'$i
done  

