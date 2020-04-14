"""
    Discord Bot to control your physical room
    Copyright (C) 2020 MorgVerd

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

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
