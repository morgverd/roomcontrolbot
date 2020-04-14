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
from discord.ext.commands import has_permissions, MissingPermissions
import urllib, random
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, brief="admin|cmd number", description="Cut x amount of messages from the channel. Useful to quickly delete spam etc.")
    async def cut(self, ctx, limit: int = 1):
        await self.bot.safe_delete(ctx.message)

        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            await ctx.channel.purge(limit=limit)
            await ctx.send('``{}`` messages were cleared by {}'.format(limit, ctx.author.mention), delete_after=20)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return

    @commands.command(pass_context=True, brief="admin|cmd word", description="Ban any word from the Filtering system. Blocking words from the SAY command. Should be used with Caution, The word must be more than 2 letters, not have any spaces, not have any newlines.")
    async def banword(self, ctx, word: str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)

        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            if word == "UNDEFINED":
                await ctx.send(embed=(await self.bot.generate_error(self, "You must define the word you wish to ban")), delete_after=20)
                return

            if " " in word: 
                await ctx.send(embed=(await self.bot.generate_error(self, "Only words can be banned, Not sentences")), delete_after=20)
                return

            if "\n" in word: 
                await ctx.send(embed=(await self.bot.generate_error(self, "Only words can be banned, No new lines")), delete_after=20)
                return

            if len(word) <= 2: 
                await ctx.send(embed=(await self.bot.generate_error(self, "The word must be more than 2 letters long")), delete_after=20)
                return

            file = open(self.bot.config["rootpath"] + "/data/badwords.txt", "a+")
            file.write(word + "\n")
            print("[ADMIN][BANWORD] Appended '" + str(word) + "' to banned word list")
            self.bot.blacklistedwords = [] # Make it remake the list
            print("[ADMIN][BANWORD] Blacklistedwords Length: " + str(len(self.bot.blacklistedwords)))
            await ctx.send(embed=(await self.bot.generate_embed(self, title=("Successfully banned ||" + str(word) + "||"), footer=f"From {ctx.message.author.name}")), delete_after=20)
            return

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return           

    @commands.command(pass_context=True, brief="admin|cmd @usr", description="Ban a user from talking in any text channel.")
    async def chatban(self, ctx, *, user: discord.Member = None):
        await self.bot.safe_delete(ctx.message)

        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            if str(self.bot.user.id) == str(user.id): return
            if user is None:
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage! Use the ``help`` command for more infomation!")), delete_after=20)
                return

            if (await self.bot.permissions_userchatmuted(self, user)):
                # Already muted
                await ctx.send(embed=(await self.bot.generate_error(self, "That user is already chatbanned. To unban them use the ``chatunban`` command")), delete_after=20)
                return

            f=open((self.bot.config["rootpath"] + "/data/users/mute/" + str(user.id)), "w+")
            f.write("1")
            f.close()

            await ctx.send(embed=(await self.bot.generate_embed(self, title=("Successfully banned " + str(user.name) + " from the chat"), footer=f"Banned by {ctx.message.author.name}")), delete_after=20)
            return

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return    


    @commands.command(pass_context=True, brief="admin|cmd @usr", description="Unban a user from talking in any text channel.")
    async def chatunban(self, ctx, *, user: discord.Member = None):
        await self.bot.safe_delete(ctx.message)

        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            if str(self.bot.user.id) == str(user.id): return
            if user is None:
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage! Use the ``help`` command for more infomation!")), delete_after=20)
                return

            if not (await self.bot.permissions_userchatmuted(self, user)):
                # Already muted
                await ctx.send(embed=(await self.bot.generate_error(self, "That user is not chatbanned. To ban them use the ``chatban`` command")), delete_after=20)
                return

            os.system("rm -rf " + (self.bot.config["rootpath"] + "/data/users/mute/" + str(user.id)))

            await ctx.send(embed=(await self.bot.generate_embed(self, title=("Successfully unbanned " + str(user.name) + " from the chat"), footer=f"Unbanned by {ctx.message.author.name}")), delete_after=20)
            return

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return   

def setup(bot):
    bot.add_cog(Admin(bot))