
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