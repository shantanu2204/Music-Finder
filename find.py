import youtube_dl
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
#import urllib
u_a = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"

http_proxy=""
proxyDict={"http":http_proxy}

print "Press 1 for search by lyrics"
print "Press 2 for search by song and artist name"
choice=input("Choose your option: ")

if choice==1:
    lyrics=raw_input("Enter the lyrics: ")
    param={'lyricText':lyrics}
    url="http://api.chartlyrics.com/apiv1.asmx/SearchLyricText"
    url1=url    
    url+="?lyricText="+lyrics
elif choice==2:
    artist=raw_input("Enter the artist name: ")
    song=raw_input("Enter the song name: ")
    param={'artist':artist, 'song':song}
    url="http://api.chartlyrics.com/apiv1.asmx/SearchLyric"
    url1=url

r=requests.get(url1, params=param, headers={"USER-AGENT":u_a})

#print r.content
#if r.status_code==200:
"""
driver=webdriver.Ie()
driver.get(url)
time.sleep(5)
source=driver.page_source
driver.quit()
"""
source=r.content
soup=BeautifulSoup(source, 'html.parser')
for p in soup(["style", "a", "span"]):
    p.extract()
songs=soup.find_all('song')
for p in xrange(len(songs)):
    songs[p]=str(songs[p].string)
artists=soup.find_all('artist')
for p in xrange(len(artists)):
    artists[p]=str(artists[p].string)
print "\nPossible Songs (Select any one):\n"
for p in xrange(len(songs)):
    print p+1,". ",songs[p]," by ",artists[p]
select=input("Enter your choice: ")
search=songs[select-1]+" "+artists[select-1]
youtube="https://www.youtube.com/results"
par={'search_query': search}

req=requests.get(youtube, params=par, headers={"USER-AGENT":u_a})
"""
driver2=webdriver.Ie()
driver2.get(youtube)
ytsource=driver2.page_source
driver2.quit()
"""
ytsource=req.content
ytsoup=BeautifulSoup(ytsource, 'html.parser')
link=re.compile(r'/watch\?v=')
mylist=ytsoup.find_all('a', 'yt-uix-tile-link', href=link)

details=[(p.text.encode('utf-8'), p.get('href')) for p in mylist]
print "\nAvailable Links:\n"
for p in (xrange(len(details))):
    print p+1,". ", details[p][0]

select=input("Enter your choice: ")
vid="www.youtube.com"+details[select-1][1]
vidurl="https://"+vid

ydl_opts = {
    '-x'
    'format': 'bestaudio',
}

ydl=youtube_dl.YoutubeDL(ydl_opts)
ydl.download([vidurl])
