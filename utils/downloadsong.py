import urllib, random
import ast, traceback, sys
import gtts
import os
import alsaaudio
import colorama; from colorama import Fore, Style
from pytube import YouTube
import pytube
import pathlib
import time

print("Preparing download")
url = (sys.argv[1])
path = (sys.argv[2])
print("URL: " + url)
print("PATH: " + path)

errVal = "0"

try:
	ytInstance = YouTube(url)
	streams = (ytInstance.streams.filter(only_audio=True))
	streams.first().download(output_path=path, filename="video")
	errVal = "1"
except Exception as err:
	print(err)
	
print("Return Value: " + errVal)
os.system("echo '" + errVal + "' >> " + path + "downloaded.txt")
time.sleep(3)
print("Exiting...")
