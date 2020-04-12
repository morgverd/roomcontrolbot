
import discord, asyncio
from discord.ext import commands
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs
from utils.filters import Filters
from utils import handlehttp

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['speak'], brief="HIDDEN", description="HIDDEN")
    async def help(self, ctx, commandHelp : str = "UNDEFINED"):
        commandsYouCanRun = []
        commandNames = {}
        cmdString = "```\n"
        allcmds = self.bot.commandsCache
        for cmd in allcmds:
            # A few sanity checks
            if not (cmd.brief == "HIDDEN"):
                if not ((cmd.brief is None) or (cmd.description is None)):
                    if ("|" in cmd.brief):
                        commandsYouCanRun.append(cmd)
                        commandNames[(cmd.name).lower()] = cmd

        if (commandHelp == "UNDEFINED"):
            # Default
            for cmd in commandsYouCanRun:
                if (len(cmd.aliases) == 0):
                    cmdString += cmd.name + "\n"
                else:
                    cmdString += (cmd.name + " - [" + (", ".join(cmd.aliases)) + "]\n")

            cmdString += "\n```"

            embed=discord.Embed(title=("Command Help"), color=(await self.bot.generate_embedcolor()))
            embed.add_field(name="Commands", value=cmdString, inline=False)
            embed.add_field(name="More Help", value="If you need more help regarding any one of those commands, Please use ``" + self.bot.config["prefix"] + "help commandname``.", inline=False)

            await ctx.send(embed=embed)
            return

        else:
            # Command info
            cmdFound = False
            for cmd in commandsYouCanRun:
                if ((cmd.name).upper() == commandHelp.upper()):
                    cmdFound = True

            if not cmdFound:
                await ctx.send(embed=(await self.bot.generate_error(self, f"``{commandHelp}`` wasn't found as a valid command, (Or at least one that you can use).\nTry using: ``" + self.bot.config["prefix"] + "help`` to view all the valid commands.\n\nAlso remember, you can only get more infomation using the actual name of the command, Not any of the Aliases")), delete_after=20)
                return

            cmd = commandNames[(commandHelp).lower()]
            cmdInfo = {}
            cmdInfo["rawinfo"] = ((cmd.brief).split("|"))
            cmdInfo["aliases"] = cmd.aliases
            if (len(cmdInfo["rawinfo"]) == 3):
                if (((cmdInfo["rawinfo"][2]).upper()) == "NSFW"):
                    cmdInfo["nsfw"] = True
            else:
                cmdInfo["nsfw"] = False
            if ((cmdInfo["rawinfo"][0]) == "*"):
                cmdInfo["everyonecanuse"] = True
                cmdInfo["roleNeeded"] = ""
            else:
                cmdInfo["everyonecanuse"] = False
                cmdInfo["roleNeeded"] = (cmdInfo["rawinfo"][0])
            cmdInfo["desc"] = cmd.description
            cmdInfo["cog"] = cmd.cog_name

            if (not (cmdInfo["everyonecanuse"])):
                # Not everyone can use
                check, __ = (await self.bot.permissions_hasrole(self, ctx.message.author, str(cmdInfo["roleNeeded"].lower())))
                if check:
                    cmdInfo["canUseCommand"] = True
                else:
                    cmdInfo["canUseCommand"] = False
            else:
                cmdInfo["canUseCommand"] = True

            cmdInfo["howtouse"] = ""
            cmdInfo["howtouse"] += self.bot.config["prefix"]
            cmdInfo["howtouse"] += ((cmdInfo["rawinfo"][1]).replace("cmd", cmd.name))

            embed=discord.Embed(title=("Info for ``" + str(cmd.name) + "``"), color=(await self.bot.generate_embedcolor()))
            embed.add_field(name="NSFW?", value=("Yes, This means that you must be in a ``NSFW`` channel to use this command since its deemed to be sexually explicit." if cmdInfo["nsfw"] is True else "No, This means that you can run this command anywhere."), inline=False)
            embed.add_field(name="Can Use Command?", value=("Yes, You possess the needed role to run this command." if cmdInfo["canUseCommand"] is True else "Sadly you're missing the role needed to run this command."), inline=False)
            embed.add_field(name="Aliases", value=((", ".join(cmdInfo["aliases"])) if (len(cmdInfo["aliases"]) == 0) is False else "There are no Aliases for this command, This means you must run the command directly."), inline=False)
            embed.add_field(name="Cog", value=(cmdInfo["cog"]), inline=False)
            embed.add_field(name="How To Use", value=cmdInfo["howtouse"], inline=False)
            embed.add_field(name="Command Description", value=cmdInfo["desc"], inline=False)
            
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))