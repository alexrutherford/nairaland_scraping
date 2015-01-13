```grab.sh > temp.txt``` Cycles through an integer range of posts, curls each, grabs the redirected URL from the returned header and writes to a file.

```python get_urls.py``` Reads the file of headers, pulls out the redirected URLS and writes to urls.txt. i.e. this maps from the form www.nairaland.com/999 => www.nairaland.com/999/post-about-bananas

```python curl_urls.py``` This reads the list of final resolved URLs from urls.txt and curls the entire content and writes to ```temp.txt```
