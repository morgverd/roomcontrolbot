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

import discord, asyncio
from discord.ext import commands
import urllib, random
import urllib.request
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs
from utils.filters import Filters
from utils import handlehttp
from bs4 import BeautifulSoup
import ast, traceback, sys
import gtts
import os
from utils import argparser
import alsaaudio
import colorama; from colorama import Fore, Style
from pytube import YouTube
import pytube
import subprocess
import pathlib
import aiohttp
from io import BytesIO
import pysubs2

class Sound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.killmusic = Funcs.killmusic # Ensure its defined for use


    @commands.command(pass_context=True, brief="canusebot|cmd message here", description="Say any message through the Bots speakers. If you're not bot staff filters will be applied to the messages you send, so dont even bother trying to say anything bad.")
    async def say(self, ctx, *, message: str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_isallowed(self, ctx.message.author))
        if permCheck:
            if (message == "UNDEFINED"):
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage. Please use ``"+self.bot.config["prefix"]+"say text``, replacing text with what you wish to say.")), delete_after=20)
                return

            adminCheck, __ = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
            if ((len(message) > 50) and (not adminCheck)):
                await ctx.send(embed=(await self.bot.generate_error(self, "You may not have more than ``50`` letters in your message. Your message had ``" + str(len(message)) + "``")), delete_after=20)
                return

            if (self.bot.videoPlaying):
                await ctx.send(embed=(await self.bot.generate_error(self, "A song is currently playing. Please use ``" + self.bot.config["prefix"] + "np`` to find out more.")), delete_after=20)
                return

            if not (self.bot.ismuted):
                originalMessage = message
                message = await self.bot.filter_englishonly(self, message)
                check, badword = await self.bot.filter_check(self, message, returnword=True)

                if adminCheck:
                    print("[SOUND][SAY] Overriding all since Admin")
                    check = True # Override
                    message = originalMessage


                if check:

                    print(Fore.CYAN + "[SOUND][SAY] " + ctx.message.author.name + "  ->  " + message + Style.RESET_ALL)
                    await self.bot.speak(self, "Message from: " + ctx.message.author.display_name + ". " + message)

                    await ctx.send(embed=(await self.bot.generate_embed(self, title=(":speaker: Saying:  ``" + (message.lower()) + "``"), footer=f"From {ctx.message.author.name}")), delete_after=20)
                    return

                else:

                    naughtyEndings = [
                        "Dont do that!",
                        "Naughty boy!",
                        "Bad boy (*spanks*)!",
                        "Cheeky!",
                        "Aren't you a bad boy?!"
                    ]
                    endmessage = naughtyEndings[random.randint(0, (len(naughtyEndings) - 1))]

                    print(Fore.YELLOW + "[SOUND][SAY] " + ctx.message.author.name + " said " + message + ", and was blocked as it contained " + badword + Style.RESET_ALL)
                    await ctx.send(embed=(await self.bot.generate_error(self, "You said something naughty.\n" + endmessage)), delete_after=20)
                    return

            else:
                await ctx.send(embed=(await self.bot.generate_error(self, ":mute: The speakers have been muted by an Admin")), delete_after=20)
                return                

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
            return

        return

    @commands.command(pass_context=True, aliases=['nowplaying', 'now'], brief="*|cmd", description="Shows the infomation regarding the song that is Now Playing. Shows how long is left, the person who requested the song, and other data about the song.")
    async def np(self, ctx):
        await self.bot.safe_delete(ctx.message)
        if not (self.bot.videoPlaying):
            await ctx.send(embed=(await self.bot.generate_error(self, "There are no songs currently playing.\nTo play a song use: ``" + self.bot.config["prefix"] + "play `` followed by a YouTube URL. Please just type ``" + self.bot.config["prefix"] + "play`` to learn more.")), delete_after=20)
            return

        rating = (str(int(float(self.bot.videoData["rating"]))) + "/5")
        embed=discord.Embed(title=self.bot.videoData["title"], color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=self.bot.videoData["thumbnail"])
        embed.add_field(name="Length", value=str(self.bot.videoData["lengthString"]), inline=True)
        embed.add_field(name="Views", value=str(self.bot.videoData["views"]), inline=True)
        embed.add_field(name="Rating", value=rating, inline=True)
        embed.add_field(name="Suggested By", value=str("<@" + str((self.bot.videoData["requester"]).id) + ">"), inline=True)

        # Stolen directly from https://github.com/Just-Some-Bots/MusicBot/blob/master/musicbot/bot.py#L1858
        # Credit to them
        prog_bar_str = ''

        percentage = 0.0
        if self.bot.videoData["length"] > 0:
            percentage = self.bot.videoCurrentTimer / self.bot.videoData["length"]

        # create the actual bar
        progress_bar_length = 30
        for i in range(progress_bar_length):
            if (percentage < 1 / progress_bar_length * i):
                prog_bar_str += '□'
            else:
                prog_bar_str += '■'


        currentMins = int(int(self.bot.videoCurrentTimer) / 60); currentSecs = int(int(self.bot.videoCurrentTimer) - int(currentMins * 60))
        prog_bar_str += "  ``" + str(currentMins) + ":" + str(currentSecs) + "``"
        prog_bar_str += " / ``" + str(self.bot.videoData["lengthString"]) + "``"

        embed.add_field(name="How Long Left?", value=str(prog_bar_str), inline=False)
        await ctx.send(embed=embed, delete_after=20)
        return


    async def searchforvideo(self, search):
        query = urllib.parse.quote(search)
        url = "https://www.youtube.com/results?search_query=" + query

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await (resp.text())

        soup = BeautifulSoup(html, "html.parser")
        arr = []
        for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
            if not vid['href'].startswith("https://googleads.g.doubleclick.net/"):
                if not "&list" in vid['href']:
                    if ("/watch?v=" in vid["href"]):
                        arr.append('https://www.youtube.com' + vid['href'])


        if len(arr) >= 3:
            return (arr[0], arr[1], arr[2])

        if (len(arr) == 0): return (None, None, None)

        return (arr[0], None, None)


    @commands.command(pass_context=True, aliases=['yt', 'music', 'song'], brief="music|cmd search terms", description="Play any song on the Bots Speakers. The video must be less than 5 minutes (unless you have the Bypass role) and must also not be age restricted. You may use ``play search term``, such as ``play megalovania ost``. Or, you can search the direct YouTube URL like so: ``play youtubeurl``. For example: ``play https://www.youtube.com/watch?v=wDgQdr8ZkTw``")
    async def play(self, ctx, *, url: str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "music"))
        if permCheck:

            if (self.bot.ismuted):
                await ctx.send(embed=(await self.bot.generate_error(self, ":mute: The speakers have been muted by an Admin")), delete_after=20)
                return

            if (self.bot.videoPlaying):
                currentMins = int(int(self.bot.videoCurrentTimer) / 60); currentSecs = int(int(self.bot.videoCurrentTimer) - int(currentMins * 60))
                await ctx.send(embed=(await self.bot.generate_error(self, "Can't play a song since another is already playing!")), delete_after=20)
                return

            if (url == "UNDEFINED"):
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage. Please use: ``" + self.bot.config["prefix"] + "play youtubeurl``.\nFor example: ``" + self.bot.config["prefix"] + "play https://www.youtube.com/watch?v=wDgQdr8ZkTw``\n\nOr, You can use ``" + self.bot.config["prefix"] + "play video search``.\nFor example: ``" + self.bot.config["prefix"] + "play megalovania OST``")), delete_after=20) # Megalovania because obvs
                return

            deleteMessage = await ctx.send(":hourglass_flowing_sand: Searching for song...")
            skipVideoInstance = False

            # Flags
            quickSearch = False
            if ("-qs" in url.lower()): quickSearch = True; url = url.replace("-qs", ""); print("[SOUND][PLAY] -qs Flag active")


            if ("youtub.be" in url.lower()):
                # mobile link
                print("[SOUND][PLAY] Was Youtu.be mobile link, Formatting into Desktop.")
                ending = (url.split("tu.be/"))[1]
                url = "https://youtube.com/watch?v=" + ending

            if (not ("youtube.com/watch?v=" in url)):
                # Do search
                print("[SOUND][PLAY] Getting urls for searchterm: " + str(url))
                urls = await self.searchforvideo(url)
                if (urls[0] == None):
                    await self.bot.safe_delete(deleteMessage)
                    await ctx.send(embed=(await self.bot.generate_error(self, "Couldn't find ``" + url + "``. Try changing your search terms?")), delete_after=20)
                    return

                if quickSearch:
                    correct = str(urls[0])
                    urls = []
                    urls.append(str(correct))
                    urls.append(None) # Dumb, but still a good skip

                if not (urls[1] == None):

                    try:
                        await deleteMessage.edit(content=":hourglass_flowing_sand: Gathering song data...")
                    except Exception:
                        pass
                    # Show options
                    urlTitles = []; lyricString = []
                    blocked = []
                    i=0
                    vidUnavailable = False
                    print("[SOUND][PLAY] Loading into ytInstance checker.")
                    ytInstances = []
                    for url in urls:
                        try:
                            try:
                                ytInstance = YouTube(url)
                                urlTitles.append(str(ytInstance.title))
                                ytInstances.append(ytInstance)
                            except pytube.exceptions.RegexMatchError:
                                await self.bot.safe_delete(deleteMessage)
                                await ctx.send(embed=(await self.bot.generate_error(self, "Failed to get URL correctly. Try again?")), delete_after=20)
                                return
                            i+=0
                        except pytube.exceptions.VideoUnavailable:
                            blocked.append(i)
                            vidUnavailable = True

                    if vidUnavailable:
                        print("[SOUND][PLAY] Video Unavailable, Skipping ask")
                        if len(urlTitles) > 0:
                            url = urls[0]
                        else:
                            await self.bot.safe_delete(deleteMessage)
                            await ctx.send(embed=(await self.bot.generate_error(self, "Couldn't get any valid links")), delete_after=20)
                            return

                    else:

                        for captionCheck in ytInstances:
                            captions = captionCheck.captions.get_by_language_code('en')
                            if captions is None:
                                lyricString.append(" ")
                            else:
                                lyricString.append(" (**Lyrics Found**) ")


                        await self.bot.safe_delete(deleteMessage)
                        embedtext = ""
                        embedtext += ":one: ``" + urlTitles[0] + "``" + lyricString[0] + "\n"
                        embedtext += ":two: ``" + urlTitles[1] + "``" + lyricString[1] + "\n"
                        embedtext += ":three: ``" + urlTitles[2] + "``" + lyricString[2] + "\n"
                        embedtext += "\n:octagonal_sign: ``None (Stop)``\n"
                        embed=discord.Embed(title="Found a few videos...", color=(await self.bot.generate_embedcolor()), description=embedtext)
                        embed.set_footer(text="If you don't choose in 20 seconds, I'll assume you dont want any")

                        embedopt = await ctx.send(embed=embed, delete_after=20)
                        await embedopt.add_reaction("1️⃣")
                        await embedopt.add_reaction("2️⃣")
                        await embedopt.add_reaction("3️⃣")
                        await embedopt.add_reaction("🛑")

                        def check(react, user): return user == ctx.message.author and (str(react.emoji) in ["1️⃣", "2️⃣", "3️⃣", "🛑"])
                        failed = False

                        try:
                            reaction, user = await self.bot.wait_for("reaction_Add", timeout=20, check=check)
                        except Exception:
                            failed = True
                            return

                        await self.bot.safe_delete(embedopt)
                        if (reaction is None): failed = True
                        if failed:
                            await ctx.send(embed=(await self.bot.generate_error(self, "I dont have all day, And you took too long. Try to run the same command but be a bit snappier?")), delete_after=20)
                            return
                        reaction = reaction.emoji # Get emoji
                        print("[SOUND][PLAY] User chose reaction: " + reaction)
                        if (reaction == "1️⃣"):
                            url = urls[0]; ytInstance = ytInstances[0]
                        elif (reaction == "2️⃣"):
                            url = urls[1]; ytInstance = ytInstances[1]
                        elif (reaction == "3️⃣"):
                            url = urls[2]; ytInstance = ytInstances[2]
                        elif (reaction == "🛑"):
                            # Quit
                            await ctx.send(embed=(await self.bot.generate_embed(self, title="You decided to Quit by pressing '🛑'. Well... Cya!", footer=f"For {ctx.message.author.name}")), delete_after=20)
                            return
                        else:
                            await ctx.send(embed=(await self.bot.generate_error(self, "I dont have all day, And you took too long. Try to run the same command but be a bit snappier?")), delete_after=20)
                            return

                        deleteMessage = await ctx.send(":hourglass_flowing_sand: Loading song data...")
                        skipVideoInstance = True



                else:
                    url = urls[0]



            if not skipVideoInstance:
                try:
                    ytInstance = YouTube(url)
                except pytube.exceptions.RegexMatchError:
                    # Invalid URL
                    await self.bot.safe_delete(deleteMessage)
                    await ctx.send(embed=(await self.bot.generate_error(self, "The YouTube URL you entered was not valid.")), delete_after=20)
                    return
            

            mins = int(int(ytInstance.length) / 60); seconds = int(int(ytInstance.length) - int(mins * 60))

            if (int(ytInstance.length) > (6 * 60)):
                permCheck, err = (await self.bot.permissions_isowner(self, ctx.message.author))
                # If its longer than 5 minutes
                if not permCheck:
                    permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "bypassmusiclimit"))
                    if not permCheck:
                        await self.bot.safe_delete(deleteMessage)
                        await ctx.send(embed=(await self.bot.generate_error(self, f"Your song is too long. The longest you can play is ``5:00`` minutes.\nYour song is ``{mins}:{seconds}``.")), delete_after=20)
                        return

            if (ytInstance.age_restricted):
                permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
                # If its age restricted
                if not permCheck:
                    await self.bot.safe_delete(deleteMessage)
                    await ctx.send(embed=(await self.bot.generate_error(self, "Your video (||" + (ytInstance.title) + "||) is age restricted, And cannot be played.\nIf you belive this to be an error please contact an Admin who can play the song for you.")), delete_after=20)
                    return

            captions = ytInstance.captions.get_by_language_code('en')
            subtitles = []
            if not captions is None:
                print("[SOUND][PLAY] Captions exist")
                self.bot.subtitlesexist = True
                captions = captions.generate_srt_captions()
                with open(self.bot.config["rootpath"] + "/data/subtiles.srt", "w") as fp: fp.write(captions) # Dump subtiles, mainly for debug
                pysubs2.make_time(s=1)
                subs = pysubs2.load(self.bot.config["rootpath"] + "/data/subtiles.srt")
                subtitles = []
                for i in range(len(subs)):
                    subtitles.append(subs[i].text)

            else:
                print("[SOUND][PLAY] Captions don't exist")
                self.bot.subtitlesexist = False
                subs = None




            self.bot.videoData["captions"] = subtitles
            self.bot.videoData["thumbnail"] = str(ytInstance.thumbnail_url)
            self.bot.videoData["title"] = str(ytInstance.title)
            self.bot.videoData["length"] = int(ytInstance.length)
            self.bot.videoData["views"] = int(ytInstance.views)
            self.bot.videoData["description"] = str(ytInstance.description)
            self.bot.videoData["rating"] = str(ytInstance.rating)
            self.bot.videoData["lengthString"] = str(str(mins) + ":" + str(seconds))
            self.bot.videoData["requester"] = ctx.message.author

            streams = (ytInstance.streams.filter(only_audio=True))
            path = (self.bot.config["rootpath"] + "/data/")
            try:
                await deleteMessage.edit(content=":hourglass_flowing_sand: Downloading song...")
            except Exception:
                pass
            print("[SOUND][PLAY] About to download: " + str(ytInstance.title))
            emojis = ["hourglass", "hourglass_flowing_sand"]
            emojiCounter = 0

            #streams.first().download(output_path=path, filename="video") # Actually do download

            if ((pathlib.Path(self.bot.config["rootpath"] + "/data/downloaded.txt")).exists()): os.system("rm -f " + self.bot.config["rootpath"] + "/data/downloaded.txt")
            os.system("lxterminal -e python3 " + self.bot.config["rootpath"] + "/utils/downloadsong.py '"+url+"' '" + path + "'")

            maxCount = 0
            print("[SOUND][PLAY] Entering waiting loop for install")
            while (not ((pathlib.Path(self.bot.config["rootpath"] + "/data/downloaded.txt")).exists())):
                if maxCount > 60:
                    await self.bot.safe_delete(deleteMessage)
                    await ctx.send(embed=(await self.bot.generate_error(self, "Song took too long to install.")), delete_after=20)
                    return

                maxCount += 1
                if emojiCounter == 0:
                    emoji = emojis[0]
                    emojiCounter = 1
                else:
                    emoji = emojis[1]
                    emojiCounter = 0

                try:
                    await deleteMessage.edit(content=":" + emoji + ": Downloading song...\nGive up in: ``" + str(maxCount) + "/60``")
                except Exception:
                    pass
                await asyncio.sleep(1)

            fileContent = ""
            with open(self.bot.config["rootpath"] + "/data/downloaded.txt", "r") as f:
                fileContent = str((f.read()).replace("\n", ""))

            print("[SOUND][PLAY] Got back: " + fileContent)
            if (fileContent == "0"):
                await self.bot.safe_delete(deleteMessage)
                await ctx.send(embed=(await self.bot.generate_error(self, "Couldn't complete install even after it was pushed to the download handle.")), delete_after=20)
                return

            # Exists
            os.system("rm -f " + self.bot.config["rootpath"] + "/utils/downloaded.txt")


            await self.bot.safe_delete(deleteMessage)

            if not ((pathlib.Path(self.bot.config["rootpath"] + "/data/video.mp4")).exists()):
                await ctx.send(embed=(await self.bot.generate_error(self, "Failed to download the song correctly. This is usually YouTubes fault. Please retry.")), delete_after=20)
                return

            embed=discord.Embed(title=self.bot.videoData["title"], color=(await self.bot.generate_embedcolor()))
            embed.set_image(url=self.bot.videoData["thumbnail"])
            embed.add_field(name="Length", value=f"{mins}:{seconds}", inline=True)
            embed.add_field(name="Views", value=str(self.bot.videoData["views"]), inline=True)

            if (self.bot.subtitlesexist):
                embed.add_field(name="Lyrics", value="You're lucky, It just so happens that the person / people who made this song went out of their way to include Lyric Captions on the video!\n\nUse ``" + self.bot.config["prefix"] + "lyrics`` to view the assosiated lyrics.", inline=False)
            else:
                embed.add_field(name="Lyrics", value="Sadly the maker of this song didn't bother to create Lyric Captions so I cant get em' for you. My appologies.", inline=False)
                
            embed.set_footer(text="Now Playing...")

            await ctx.send(embed=embed, delete_after=20)
            activity = discord.Activity(name=(self.bot.videoData["title"]), type=discord.ActivityType.listening)
            await self.bot.change_presence(activity=activity)

            self.bot.videoPlaying = True
            self.bot.videoCurrentTimer = 0

            # Important part
            os.system("lxterminal -e vlc --audio "+ self.bot.config["rootpath"] +"/data/video.mp4")

            print("[SOUND][PLAY] Starting "+ str(ytInstance.length) +" second song timer for " + ytInstance.title)
            for i in range(int(ytInstance.length) + 2):
                # Do waiting loop, 2 second buffer
                await asyncio.sleep(1)
                self.bot.videoCurrentTimer = self.bot.videoCurrentTimer + 1
                if not self.bot.videoPlaying: break
            print(Fore.GREEN + "[SOUND][PLAY] Finished song timer for " + ytInstance.title + Style.RESET_ALL)
            
            await self.bot.killmusic(self) # Kill all music

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
            return

    @commands.command(pass_context=True, aliases=['subs', 'subtiles'], brief="*|cmd", description="Shows the Lyrics for the current song (If there are any). They may not always be accurate considering they are pulled from the YouTube captions.")
    async def lyrics(self, ctx):
        await self.bot.safe_delete(ctx.message)
        if not (self.bot.videoPlaying):
            # Song isnt playing
            await ctx.send(embed=(await self.bot.generate_error(self, "There are no songs playing!")), delete_after=20)
            return

        if not (self.bot.subtitlesexist):
            # Subtiles do not exist
            await ctx.send(embed=(await self.bot.generate_error(self, "There are no saved Lyrics for this song.")), delete_after=20)
            return
        
        counter = 0; firstCycle = True; msg = None
        pysubs2.make_time(s=1)
        allsubtitles = self.bot.videoData["captions"]

        letterCounter = 0
        letterBlock = 0
        letterBlocks = {}
        currentBlock = []
        currentBlock.append("Lyrics for '" + self.bot.videoData["title"] + "' as requested by '" + (self.bot.videoData["requester"]).name + "'.\n(These Lyrics are straight from the YouTube video provided, so any issues are the fault of the uploader, Not us)\n\n")
        for line in allsubtitles:
            letterCounter += len(line)
            currentBlock.append(line)
            if letterCounter > 500:
                letterBlocks[str(letterBlock)] = currentBlock
                letterBlock += 1
                currentBlock = []
                letterCounter = 0

        if not (len(currentBlock) == 0):
            letterBlocks[str(letterBlock)] = currentBlock
            letterBlock += 1

        for i in range(letterBlock):
            block = letterBlocks[str(i)]
            string = ("\n".join(block))
            await ctx.send("```\n" + string + "\n```")


        return

    @commands.command(pass_context=True, brief="admin|cmd", description="Stops the current song from playing. Also resets the music player.")
    async def stop(self, ctx):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "music"))
        if permCheck:

            if not (self.bot.videoPlaying):
                # Song isnt playing
                await ctx.send(embed=(await self.bot.generate_error(self, "There are no songs playing!")), delete_after=20)
                return

            else:
                # do before destroying
                oldTitle = str(self.bot.videoData["title"])
                await self.bot.killmusic(self) # Kill all music
                await ctx.send(embed=(await self.bot.generate_embed(self, title=":octagonal_sign: ``" + oldTitle + "`` has been stopped.", footer=f"From {ctx.message.author.name}")), delete_after=20)
                


        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
        return


    async def setvol(self, v): os.system("amixer set PCM -- " + str(v) + "%")
    async def getvol(self):
        m = alsaaudio.Mixer("PCM")
        vol = (m.getvolume())[0]
        return int(vol)

    @commands.command(pass_context=True, aliases=['vol'], brief="admin|cmd percent", description="Sets the system volume for songs etc. Must be more than ``%1`` and less than ``100%``. You may also just use the raw command ``volume`` to get the current volume.")
    async def volume(self, ctx, vol:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            if (self.bot.ismuted):
                await ctx.send(embed=(await self.bot.generate_error(self, ":mute: The speakers have been muted by an Admin")), delete_after=20)
                return

            if vol == "UNDEFINED":
                await ctx.send(embed=(await self.bot.generate_embed(self, title=":speaker: The volume is currently at ``" + str(await self.getvol()) + "%``")), delete_after=20)   
                return

            # Dumb, ik but it works
            try:
                vol = int(vol)
                # Test if its a number
                x = vol+1
                y = vol-3
            except Exception:
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage. Please use ``"+self.bot.config["prefix"]+"vol`` followed by a number from 1 to 100.\nFor example: ``"+self.bot.config["prefix"]+"vol 50``")), delete_after=20)
                return

            if vol > 100:
                await ctx.send(embed=(await self.bot.generate_error(self, "Volume cannot be set to more than ``100%``")), delete_after=20)
                return

            if vol < 1:
                await ctx.send(embed=(await self.bot.generate_error(self, "Volume cannot be set to less than ``1%``")), delete_after=20)
                return

            print("[SOUND][VOL] " + ctx.message.author.name + " has updated the volume to " + str(vol) + "%")
            await self.setvol(int(vol))
            self.bot.lastVolume = int(vol)
            await ctx.send(embed=(await self.bot.generate_embed(self, title=":speaker: The volume was set to ``" + str(await self.getvol()) + "%``")), delete_after=20) 

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
        return

    @commands.command(pass_context=True, aliases=['unmute', 'shutup'], brief="admin|cmd", description="Mutes/Unmutes the speakers")
    async def mute(self, ctx):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            m = alsaaudio.Mixer('PCM')
            current_vol = (m.getvolume())[0]
           
            if not (self.bot.ismuted):
                print(Fore.CYAN + "[SOUND][MUTE] " + ctx.message.author.name + " has just muted the speakers" + Style.RESET_ALL)
                # Mute
                await ctx.send(embed=(await self.bot.generate_embed(self, title=":mute: Speakers have been muted", footer=f"From {ctx.message.author.name}")), delete_after=20)
                m.setvolume(0) # Off
                await self.setvol(0) # Off
                self.bot.ismuted = True
                return
            else:
                print(Fore.CYAN + "[SOUND][UNMUTE] " + ctx.message.author.name + " has just unmuted the speakers" + Style.RESET_ALL)
                # Unmute
                await ctx.send(embed=(await self.bot.generate_embed(self, title=":speaker: Speakers have been unmuted", footer=f"From {ctx.message.author.name}")), delete_after=20)
                if not (self.bot.lastVolume == 0):
                    print("[SOUND][MUTE] Going back to lastVolume: " + str(self.bot.lastVolume))
                    m.setvolume(self.bot.lastVolume) # On
                    await self.setvol(self.bot.lastVolume)
                else:
                    print("[SOUND][MUTE] Couldn't get lastVolume, Defaulting to 50")
                    m.setvolume(50) # On
                    await self.setvol(50) # Default
                self.bot.ismuted = False
                return


        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)), delete_after=20)
        return

def setup(bot):
    bot.add_cog(Sound(bot))