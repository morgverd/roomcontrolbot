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

import asyncio, aiohttp, aiosocks, discord, async_timeout, pytz, time
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time, jsonpickle
from datetime import datetime
import colorama; from colorama import Fore, Style

class Filters():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.session = aiohttp.ClientSession()


    async def filter_englishonly(self, message):
        eng = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ ") # Make sure Spaces are in there
        engOnly = []
        for i in range(len(message)):
            letter = list(message)[i]
            if (letter.upper()) in eng:
                engOnly.append(letter)
        return "".join(engOnly)

    async def filter_check(self, message, returnword:bool = False):
        bot = self.bot
        try:
            msg = message.content
        except Exception:
            msg = message

        if (len(bot.blacklistedwords) == 0):
            badwords = []
            with open(self.bot.config["rootpath"] + "/data/badwords.txt", "r") as f: content = f.readlines()
            for line in content:
                line = line.replace("\n", "") # Replace new line strings
                line = line.replace(" ", "") # Work word by word basis
                if len(line) > 2: badwords.append(line.upper()) # Stpp very small words from blocking text
                
            bot.blacklistedwords = badwords
            print(Fore.GREEN + f"[FILTERS] Initialised filterlist with {str(len(bot.blacklistedwords))} words." + Style.RESET_ALL)

        msg = msg.upper() # Important for comparison
        msg = msg.replace(" ", "") # One string
        
        i=0
        for word in (bot.blacklistedwords):
            # Each word
            if (word.upper()) in msg:
                if returnword:
                    return (False, (word.upper()))
                else:
                    return False
            i+=1
        if returnword:
            return (True, "")
        else:
            return True



def setup(bot):
    bot.add_cog(Filters(bot))