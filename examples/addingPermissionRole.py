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

# Do basic imports
import discord, asyncio
from discord.ext import commands
import urllib, random
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs

# Below is an example of what your config.json roleIDs section may look like.
"""
	"roleIDs" : {
		"admin" : 675427918066745425,
		"music" : 675889984699498506,
		"canusebot" : 675398247136624651,
		"bypassmusiclimit" : 676135918268186665 
	},
"""

# To add your new role to the permissions system.
"""
	"roleIDs" : {
		"admin" : 675427918066745425,
		"music" : 675889984699498506,
		"canusebot" : 675398247136624651,
		"bypassmusiclimit" : 676135918268186665,
		"mycustomrole" : 674615632741793792
	},
"""

# You first define the name of the new role and then the ID of the role in question.
# Then you can call it as such.

# Change Example to whatever your Cog file is called
class Example(commands.Cog):
    # Copy exactly
    def __init__(self, bot):
        self.bot = bot
        # You can also define any other variables or functions you wish to use a lot here

    # See https://github.com/morgverd-1/roomcontrolbot#example-command-with-comments-explaining-usage-cases- for help, Or the commandexample.py file.
    # You should add your custom role to the breif.
    @commands.command(pass_context=True, brief="mycustomrole|cmd", description="Example Command")
    async def doesuserhaverole(self, ctx):
    	permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "mycustomrole")) # Check if the user has the role defined above called "mycustomrole"
    	if permCheck:
    		# User has the role with the ID specificed next to "mycustomrole"
    		await ctx.send("You have the role!") # Say something (for example)

    	else:
    		# User doesnt have the role, Error message in err
    		await ctx.send(embed=(await self.bot.generate_error(self, err))) # Generate an error message with the text being the variable err that contains our error message

    	return


def setup(bot):
    # Like above, Change Example to the name of your Cog
	bot.add_cog(Example(bot))
	