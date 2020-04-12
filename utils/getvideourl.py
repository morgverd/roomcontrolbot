import urllib.request
from bs4 import BeautifulSoup
import pathlib
import ast, traceback, sys


textToSearch = (sys.argv[1])
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib.request.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
arr = []
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
    	if not "&list" in vid['href']:
    		arr = ('https://www.youtube.com' + vid['href'])
