
import asyncio, aiohttp, aiosocks, discord, async_timeout, pytz, time
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time, jsonpickle
from datetime import datetime
import os.path


class Permissions():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.tz = pytz.timezone('UTC')

    async def permissions_isowner(self, user):
        userid = user.id
        if userid == (self.bot.config["ownerID"]): return (True, "User is the Owner")
        return (False, "Only the Owner may do this.")

    async def permissions_hasrole(self, user, rolename):
        bot = self.bot
        isowner, __ = await bot.permissions_isowner(self, user)
        if isowner: return (True, "User is the Owner")
        if rolename.lower() == "canusensfw":
            # Check configuration to see if a role is required
            if bot.config["requireNSFWrole"] == "FALSE":
                # Role not needed
                return (True, "NSFW role is not required in Config")
        # Check that the role is valid
        try:
            roleid = str(bot.config["roleIDs"][rolename])
        except Exception:
            print("[PERMISSIONS] Role '" + rolename + "' Doesn't exist")
            return (False, (rolename + " doesnt Exist"))
        for role in user.roles:
            if (roleid == str(role.id)): return (True, "User has role")
        return (False, "You are missing the needed role to do this.")

    async def permissions_isallowed(self, user):
        bot = self.bot
        isowner, __ = await bot.permissions_isowner(self, user)
        if (isowner): return (True, "User is the Owner")
        if (await bot.permissions_restrictedtime(bot)): return (False, (f"You may only use me inbetween {str(bot.config["minimumtime"])} and {str(bot.config["maximumtime"])}. Sorry!")) # Time is bad
        if (await bot.permissions_hasrole(self, user, "canusebot")): return (True, "User has role")
        return (False, "You are missing the needed role to do this.")

    async def permissions_restrictedtime(bot):
        hour = int(time.strftime("%H"))
        if ((hour > int(bot.config["allowedtimes"]["maximumtime"])) or (hour < int(bot.config["allowedtimes"]["minimumtime"]))): return False
        return True


    async def permissions_userchatmuted(x, user, takeBot=False):
        if takeBot:
            bot = x
        else:
            bot = x.bot
        if os.path.isfile(bot.config["rootpath"] + "/data/users/mute/" + str(user.id)):
            # File exists, User is chat muted
            return True
        else:
            return False

    async def permissions_userlivebanned(self, user):
        bot = self.bot
        if os.path.isfile(self.bot.config["rootpath"] + "/data/users/nolive/" + str(user.id)):
            # File exists, User is banned from going live
            return True
        else:
            return False        



def setup(bot):
    bot.add_cog(Permissions(bot))