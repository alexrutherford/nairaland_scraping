```grab.sh > temp.txt``` Cycles through an integer range of posts, curls each, grabs the redirected URL from the returned header and writes to a file.

```python get_urls.py``` Reads the file of headers, pulls out the redirected URLS and writes to urls.txt. i.e. this maps from the form www.nairaland.com/999 => www.nairaland.com/999/post-about-bananas

```python curl_urls.py``` This reads the list of final resolved URLs from urls.txt and curls the entire content and writes to ```temp.txt```   

Some posts were lost in hacking attack e.g. http://www.nairaland.com/1978886/ All posts were lost between the dates of 10th Jan and 22nd June 2014.

Number 2068873 corresponds to 30th December   

Number 1973874 corresponds to 30th October  

Number 1913874 corresponds to 21st Sep  

Number 1811873 corresponds to 14th July


Grabbed pages begin at http://www.nairaland.com/1788360/nairaland-back (25th June) and end at http://www.nairaland.com/2068873/please-ooo-me-answer-oo (December 30th)


Second batch from same time period in 2013 http://www.nairaland.com/1306341/atheists-explain-how-religious-peeps to http://www.nairaland.com/1569917/lady-girl-good-farting
