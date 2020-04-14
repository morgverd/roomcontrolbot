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

import asyncio, aiohttp, discord
import PIL, PIL.Image, PIL.ImageFont, PIL.ImageOps, PIL.ImageDraw
import numpy as np
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import urllib, random
import urbandict
import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
from urllib.parse import quote
from io import BytesIO
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs
from utils import handlehttp, argparser
import simplejson
from requests.utils import requote_uri

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_json = bot.get_json
        self.get_text = bot.get_text

    async def randomimageapi(self, ctx, url, endpoint, animal):
        error = False
        try:
            url = requote_uri(url)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as responce:
                    if responce.status == 200:
                        r = (await responce.json(content_type="text/html"))
                    else:
                        error = True

        except simplejson.errors.JSONDecodeError:
            error = True

        if error:
            await ctx.send(embed=(await self.bot.generate_error(self, "An error occured with the API.")), delete_after=20)
            return

        embed=discord.Embed(title="For " + ctx.message.author.name + ". Heres your " + animal, color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(r[endpoint]))
        await ctx.send(embed=embed)


    async def api_img_creator(self, ctx, url, filename, content=None):
        async with ctx.channel.typing():
            req = await handlehttp.get(url, res_method="read")

            if req is None:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))


    @commands.command(aliases=["meow"], brief="*|cmd", description="Get a cute cat picture")
    async def cat(self, ctx):
        await self.bot.safe_delete(ctx.message)
        """ Posts a random cat """
        await self.randomimageapi(ctx, f'https://cdn.morgverd.xyz/botapi/animals/?k={self.bot.config["apiKey"]}&a=cat', 'file', 'cat')

    @commands.command(aliases=["woof"], brief="*|cmd", description="Get a cute dog picture")
    async def dog(self, ctx):
        await self.bot.safe_delete(ctx.message)
        """ Posts a random dog """
        await self.randomimageapi(ctx, f'https://cdn.morgverd.xyz/botapi/animals/?k={self.bot.config["apiKey"]}&a=dog', 'file', 'dog')

    @commands.command(aliases=["bird", "oiseau", "tweettweet"], brief="*|cmd", description="Get a cute bird picture")
    async def birb(self, ctx):
        await self.bot.safe_delete(ctx.message)
        """ Posts a random birb """
        await self.randomimageapi(ctx, f'https://cdn.morgverd.xyz/botapi/animals/?k={self.bot.config["apiKey"]}&a=bird', 'file', 'birb')

    @commands.command(aliases=["quack"], brief="*|cmd", description="Get a cute duck picture")
    async def duck(self, ctx):
        await self.bot.safe_delete(ctx.message)
        """ Posts a random duck """
        await self.randomimageapi(ctx, f'https://cdn.morgverd.xyz/botapi/animals/?k={self.bot.config["apiKey"]}&a=duck', 'file', 'duck')

    @commands.command(brief="*|cmd text", description="Turn any text into a Supreme Logo. You may add ``-d`` to your text to make it Dark Themed, or ``-l`` to make it a lighter theme.")
    async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True) = "UNDEFINED"):
        """ Make a fake Supreme logo
        Arguments:
            --dark | Make the background to dark colour
            --light | Make background to light and text to dark colour
        """
        await self.bot.safe_delete(ctx.message)

        if (text=="UNDEFINED"): text = (ctx.message.author.name) # Default text to name 
        
        parser = argparser.Arguments()
        parser.add_argument('input', nargs="+", default=None)
        parser.add_argument('-d', '--dark', action='store_true')
        parser.add_argument('-l', '--light', action='store_true')

        args, valid_check = parser.parse_args(text)
        if not valid_check:
            return await ctx.send(args)

        inputText = urllib.parse.quote(' '.join(args.input))
        if len(inputText) > 500:
            return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

        darkorlight = ""
        if args.dark:
            darkorlight = "dark=true"
        if args.light:
            darkorlight = "light=true"
        if args.dark and args.light:
            return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

        await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png")


    @commands.command(aliases=['howhot', 'hot'], brief="*|cmd @usr", description="Scientically calculate how hot someone is. Based upon the username.")
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        await self.bot.safe_delete(ctx.message)
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(pass_context=True, aliases=["template", "meme"], brief="*|cmd", description="Get a random meme template from imgflip.")
    async def memetemplate(self, ctx, direct=None):
        await self.bot.safe_delete(ctx.message)
        load = await self.get_json("https://api.imgflip.com/get_memes")
        url = random.choice(load['data']['memes'])
        url = url['url']

        embed=discord.Embed(title="For " + ctx.message.author.name + ". Heres your bad meme template", color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(url))
        
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, brief="*|cmd search", description="Search the Urban Dictionary for any search term. Useful if you're being a boomer.")
    async def urban(self, ctx, *, word:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)

        if (word == "UNDEFINED"): await ctx.send(embed=(await self.bot.generate_error(self, "To use this command please use ``"+self.bot.config["prefix"]+"urban word`` and swap out ``word`` for the word you wish to define!")), delete_after=20); return

        urb = urbandict.define(word)
        if "There aren't any definitions" in urb[0]['def']:
            await self.bot.say(":no_mouth: `No definition found.`")
            return

        embed=discord.Embed(title="Urban Dictionary", color=(await self.bot.generate_embedcolor()))
        embed.set_footer(text="For " + ctx.message.author.name)
        embed.add_field(name="Search", value=str(word), inline=True)
        embed.add_field(name="Definition", value=str(urb[0]['def']), inline=False)
        embed.add_field(name="Example", value=str(urb[0]['example']), inline=False)
        await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['text2img', 'texttoimage', 'text2image'], brief="*|cmd text", description="Make any text into a Arial font image")
    async def tti(self, ctx, *, txt:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)

        if (word == "UNDEFINED"): await ctx.send(embed=(await self.bot.generate_error(self, "To use this command please use ``"+self.bot.config["prefix"]+"tti word`` and swap out ``word`` for word you wish to turn into an image.")), delete_after=20); return

        api = 'http://api.img4me.com/?font=arial&fcolor=FFFFFF&size=35&type=png&text={0}'.format(quote(txt))
        r = await self.get_text(api)

        embed=discord.Embed(title="For " + ctx.message.author.name, color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(r))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=['comicsans'], brief="*|cmd text", description="Turn any text into a Sans font image")
    async def sans(self, ctx, *, txt:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)

        if (word == "UNDEFINED"): await ctx.send(embed=(await self.bot.generate_error(self, "To use this command please use ``"+self.bot.config["prefix"]+"sans word`` and swap out ``word`` for word you wish to turn into an image.")), delete_after=20); return

        api = 'http://api.img4me.com/?font=sans&fcolor=000000&size=35&type=png&text={0}'.format(quote(txt))
        r = await self.get_text(api)


        embed=discord.Embed(title="For " + ctx.message.author.name, color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(r))
        await ctx.send(embed=embed)


    @commands.command(pass_context=True, aliases=['achievement', 'ach'], brief="*|cmd text", description="Turn any text into a Minecraft achievement")
    async def mc(self, ctx, *, txt:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)

        if (word == "UNDEFINED"): await ctx.send(embed=(await self.bot.generate_error(self, "To use this command please use ``"+self.bot.config["prefix"]+"mc word`` and swap out ``word`` for word you wish to turn into a minecraft achivement.")), delete_after=20); return

        """Generate a Minecraft Achievement"""
        api = "https://mcgen.herokuapp.com/a.php?i=1&h=Achievement-{0}&t={1}".format(ctx.message.author.name, txt)

        embed=discord.Embed(title="For " + ctx.message.author.name, color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(api))
        await ctx.send(embed=embed)

    async def safe_emojidelete(self, reaction, usr):
        try:
            await reaction.remove(usr)
        except Exception:
            pass
        return

    @commands.command(pass_context=True, aliases=['move'], brief="*|cmd @usr", description="Vote to have any user in your Voice Channel put into the AFK channel (Kick em out). Useful if someones being annoying and there aren't any staff online to help. Abuse of this command may result in Punishment.")
    async def vote(self, ctx, *, user: discord.Member = None):
        await self.bot.safe_delete(ctx.message)

        # Error checks --------------------------------------
        if user is None:
            await ctx.send(embed=(await self.bot.generate_error(self, "Please mention who should be moved!\nExample: ``"+self.bot.config["prefix"]+"vote @Someone#1111``")), delete_after=20)
            return

        if not (ctx.author.voice and ctx.author.voice.channel):
            await ctx.send(embed=(await self.bot.generate_error(self, "You're not in a voice channel")), delete_after=20)
            return

        if not (user.voice and user.voice.channel):
            await ctx.send(embed=(await self.bot.generate_error(self, "<@" + str(user.id) + "> is not in a voice channel")), delete_after=20)
            return

        if (ctx.author.id == user.id):
            await ctx.send(embed=(await self.bot.generate_error(self, "You cannot vote against yourself")), delete_after=20)
            return

        if (user.voice.channel.id == self.bot.config["afkvoice_channel"]):
            await ctx.send(embed=(await self.bot.generate_error(self, "<@" + str(user.id) + "> is already in the channel you want them to be moved into")), delete_after=20)
            return

        if not (ctx.author.voice.channel.id == user.voice.channel.id):
            await ctx.send(embed=(await self.bot.generate_error(self, "<@" + str(user.id) + "> is not in the same voice channel with you")), delete_after=20)
            return
        # End of Error Checks -------------------------------

        activeVoiceChannel = ctx.author.voice.channel
        activeChannelMembers = ctx.author.voice.channel.members
        activeChannelMembersIds = []
        for usr in activeChannelMembers: activeChannelMembersIds.append(str(usr.id))

        mayvotestring = ""
        for uid in activeChannelMembersIds:
            mayvotestring += ("<@" + uid + ">")
            mayvotestring += ", "

        embed=discord.Embed(title=("``" + ctx.author.name + "`` is voting to ban ``" + user.name + "`` from ``" + str(activeVoiceChannel.name) + "`` for ``5`` minutes."), color=(await self.bot.generate_embedcolor()))
        embed.set_image(url=str(user.avatar_url))
        embed.add_field(name="Suggested By", value=str("<@" + str(ctx.author.id) + ">"), inline=True)
        embed.add_field(name="Subject", value=str("<@" + str(user.id) + ">"), inline=True)
        embed.add_field(name="How to Vote", value=f"Just below this message you will see :white_check_mark: and :x:, Click on the related Reaction to vote on if <@{str(user.id)}> should be moved.\n\nClick on the :white_check_mark: if you vote **YES**\nClick on the :x: if you vote **NO**\n\nOnly click on the :octagonal_sign: if you're a Bot Admin and wish to stop the vote from taking place.", inline=False)
        embed.add_field(name="Rules", value=f"For your vote to count, you must be in the Voice Channel with <@" + str(ctx.author.id) + ">\n\n*If you vote for two options or keep changing votes, We will take your last vote as your final vote*\n\nOnly the following may vote:\n" + mayvotestring, inline=False)
        embed.set_footer(text="This vote will last 1 minute.")
        voteMessage = await ctx.send(embed=embed)
        await voteMessage.add_reaction("✅")
        await voteMessage.add_reaction("❌")
        await voteMessage.add_reaction("🛑")

        # Just return everything
        async def check(react, user):
            return True

        failed = False
        votes = {}
        usersEmoji = {}

        while True:
            try:
                reaction, usr = await self.bot.wait_for("reaction_Add", timeout=60, check=check)
                if reaction:
                    # Ignore bot
                    if not usr.id == self.bot.user.id:
                        if usr.voice:
                            # User is in voice channel
                            if (str(usr.id) in votes):
                                # Already reacted
                                print(str((votes[str(usr.id)]).emoji))
                                await self.safe_emojidelete(votes[str(usr.id)], usr)


                            if (str(reaction.emoji) in ["❌", "✅"]):
                                # Valid Emoji
                                print("[FUN][VOTE] " + str(usr.name) + " just reacted with " + str(reaction.emoji))
                                votes[str(usr.id)] = (reaction)

                            elif (str(reaction.emoji) == "🛑"):
                                # Admin Emoji
                                permCheck, err = (await self.bot.permissions_hasrole(self, usr, "admin"))
                                if permCheck:
                                    await self.bot.safe_delete(voteMessage)
                                    await ctx.send(embed=(await self.bot.generate_embed(self, title=(usr.name + " just stopped the vote"))), delete_after=20)
                                    return
                                else:
                                    await self.safe_emojidelete(reaction, usr)

                            else:
                                await self.safe_emojidelete(reaction, usr)

                        else:
                            await self.safe_emojidelete(reaction, usr)


            except asyncio.TimeoutError:
                break
        await self.bot.safe_delete(voteMessage)

        if (len(votes.keys()) == 0):
            await ctx.send(embed=(await self.bot.generate_error(self, "Nobody voted")), delete_after=20)
            return

        votestring = ""
        winnerString = ""
        yes = 0
        no = 0
        moveUsr = False
        def emojiToStr(emoji):
            if emoji == "✅": return "YES"
            return "NO"

        for voteid in votes.keys():
            print(voteid + " voted " + (votes[voteid].emoji))
            ans = emojiToStr((votes[voteid]).emoji)
            votestring += "<@" + voteid + "> voted **" + ans + "**\n"
            if ans.upper() == "YES": yes += 1
            if ans.upper() == "NO": no += 1

        if (yes > no):
            winnerString = "**YES** has won, <@" + str(user.id) + "> will be moved."
            moveUsr = True

        elif (no > yes):
            winnerString = "**NO** has won, <@" + str(user.id) + "> will **NOT** be moved."
            moveUsr = False

        else:
            # tie
            winnerString = "**TIE**, Nothing will happen."
            moveUsr = False


        embed=discord.Embed(title=("Results for ``" + ctx.author.name + "``'s Vote"), color=(await self.bot.generate_embedcolor()))
        #embed.set_image(url=str(user.avatar_url))
        embed.add_field(name="Suggested By", value=str("<@" + str(ctx.author.id) + ">"), inline=True)
        embed.add_field(name="Subject", value=str("<@" + str(user.id) + ">"), inline=True)
        embed.add_field(name="Votes", value=votestring, inline=False)
        embed.add_field(name="Result", value=winnerString, inline=False)

        final = await ctx.send(embed=embed, delete_after=20)

        if moveUsr:
            channel = self.bot.get_channel(self.bot.config["afkvoice_channel"])

            try:
                await member.send("You have been banned from ``" + activeVoiceChannel.name + "`` for 5 minutes.")
            except Exception:
                pass

            self.bot.bannedFromChannels.append(str(user.id))
            self.bot.bannedFromChannelID[str(user.id)] = str(activeVoiceChannel.id)

            try:
                await user.move_to(channel, reason=f"{ctx.author.name} voted to move them")
            except Exception as err:
                print("[FUN][VOTE] Coudln't move user, Do it manually")
                await ctx.send(embed=(await self.bot.generate_error(self, "Couldn't move user")), delete_after=20)

            print("[FUN][VOTE] Banning '" + user.name + "' from '" + activeVoiceChannel.name + "' for 5 minutes")
            await asyncio.sleep(60 * 5) # 5 Minutes
            print("[FUN][VOTE] Unbanning '" + user.name + "' from '" + activeVoiceChannel.name + "'")

            (self.bot.bannedFromChannels).remove(str(user.id))

            try:
                await member.send("You have been unbanned from ``" + activeVoiceChannel.name + "``.")
            except Exception:
                pass

        return




def setup(bot):
    bot.add_cog(Fun(bot))