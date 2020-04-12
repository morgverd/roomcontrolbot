
import asyncio, aiohttp, aiosocks, discord, async_timeout
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time, jsonpickle
import pathlib

class Funcs():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.config = bot.config
        self.session = aiohttp.ClientSession()

    async def get_json(url:str):
        session = aiohttp.ClientSession()
        try:
            with async_timeout.timeout(5):
                async with session.get(url) as resp:
                    try:
                        load = await resp.json()
                        return load
                    except:
                        return {}
        except asyncio.TimeoutError:
            return {}

    async def killmusic(self):
        os.system("killall vlc")
        self.bot.videoPlaying = False
        self.bot.subtitlesexist = False
        self.bot.videoData = {}

        if ((pathlib.Path(self.bot.config["rootpath"] + "/data/video.mp4")).exists()):
            # Delete the video saved
            os.system("rm -f " + self.bot.config["rootpath"] + "/data/video.mp4")

        if ((pathlib.Path(self.bot.config["rootpath"] + "/data/subtiles.srt")).exists()):
            # Delete the video saved
            os.system("rm -f " + self.bot.config["rootpath"] + "/data/subtiles.srt")

        return

    async def speak(self, message, isbot=False):
        if isbot:
            bot = self
        else:
            bot = self.bot

        os.system("lxterminal -e sh "+ bot.config["rootpath"] +"/utils/say.sh '"+str(message)+"' '"+str(bot.lastVolume)+"'")
        print("[FUNCS][SPEAK] Said: " + message)
        return

    async def safe_delete(message):
        try:
            await message.delete()
        except Exception:
            pass
        return

    async def read_raw(url:str):
        session = aiohttp.ClientSession()
        try:
            with async_timeout.timeout(5):
                async with session.get(url) as resp:
                    return resp
        except asyncio.TimeoutError:
            return False
    
    


    async def get_text(url:str):
        session = aiohttp.ClientSession()
        try:
            with async_timeout.timeout(5):
                async with session.get(url) as resp:
                    try:
                        text = await resp.text()
                        return text
                    except:
                        return False
        except asyncio.TimeoutError:
            return False
    
    