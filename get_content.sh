while read line
    echo "'"$line"'"
    do curl "'"$line"'"
        done < trash_urls.txt
