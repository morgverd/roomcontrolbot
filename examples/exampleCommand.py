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

# WARNING: This example DOESN'T WORK by itsself since there is no Cog defined or setup.
# This command is to act as part of a cog.


# First import everything we need
import discord, asyncio
from discord.ext import commands
import urllib, random
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs

# First with the command decorator
# You want to make sure that in the 'brief' argument there is always 'roleneeded|cmd usage'
# For this example, only the 'admin' role as defined in config.json can run this, So in 'brief' the first part is 'admin'
# Next, you split up each part with a |
# You then add the 'example usage'. For this you always include a lowercase 'cmd'. This is beacause it will be swapped out for the command name later on
# After command, you want a self explainatory argument. In this message we want the user to do '>>saythis hello', so we will use 'message' for our example
# If the command is NSFW, You need to make sure to add '|nsfw' to the end so the help command knows its NSFW, and to display it as such.
@commands.command(pass_context=True, brief="admin|cmd message", description="Says the message as the bot") # The decorator mentioned
async def saythis(self, ctx, *, message: str = "UwU"):
    await self.bot.safe_delete(ctx.message) # Delete the users message with safe_delete as mentioned above.
    permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin")) # This only allows users with the defined 'admin' (from config.json) to pass
    # permCheck contains a BOOL statement. TRUE means that the user does have the needed rank, FALSE means that they dont.
    # err contains the error message (if there is any)

    # Since permCheck is just BOOL we can test it here
    if permCheck:
        # If the user does have the admin role, Say their message
        await ctx.send(message)
    else:
        # permCheck is FALSE, meaning that the user does not have the needed role
        # err is used to represent the text error message that we got when we first tested for the users role
        await ctx.send(embed=(await self.bot.generate_error(self, err))) # Generate an error message with the text being the variable err that contains our error message
    return # Always return no matter what