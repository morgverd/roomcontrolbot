
import discord, asyncio
from discord.ext import commands
import urllib, random, os
from utils.generators import Generators
from utils.permissions import Permissions
import ast, traceback, sys
import colorama; from colorama import Fore, Style
import time
import pyspeedtest

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, brief="admin|cmd message", description="Says the message as the bot")
    async def echo(self, ctx, *, message: str = "UwU"):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            await ctx.send(message)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))

        return

    @commands.command(pass_context=True, brief="HIDDEN", description="HIDDEN")
    async def reboot(self, ctx):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_isowner(self, ctx.message.author))
        if permCheck:
            print(Fore.RED + "[UTILS][REBOOT] " + ctx.message.author.name + " is rebooting the bot. Triggering disconnect." + Style.RESET_ALL)
            await self.bot.close()
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))

        return

    @commands.command(pass_context=True, brief="HIDDEN", description="HIDDEN")
    async def disconnect(self, ctx):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_isowner(self, ctx.message.author))
        if permCheck:
            print(Fore.RED + "[UTILS][FATAL] " + ctx.message.author.name + " is stopping the bot. Closing." + Style.RESET_ALL)
            os.system("killall vlc")
            sys.exit(0)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))

        return

    @commands.command(pass_context=True, brief="admin|cmd url", description="Embeds a media URL into Discord from the Bot")
    async def embedurl(self, ctx, *, url: str = "https://media.tenor.com/images/df51cc9619b2afefd0fe34e697060ca8/tenor.gif"):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "admin"))
        if permCheck:
            embed=discord.Embed(color=(await self.bot.generate_embedcolor()))
            embed.set_image(url=str(url))
            embed.set_footer(text="Sent By: " + str(ctx.message.author.name))
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))

        return

    @commands.command(pass_context=True, brief="HIDDEN", description="HIDDEN")
    async def debug(self, ctx):
        await self.bot.safe_delete(ctx.message)
        permCheck, err = (await self.bot.permissions_isowner(self, ctx.message.author))
        if not permCheck: await ctx.send(embed=(await self.bot.generate_error(self, err)))

        #st = pyspeedtest.SpeedTest()
        info = await self.bot.application_info()
        lines = []
        lines.append(":stopwatch: Latency: ``" + str(self.bot.latency) + "``")
        #lines.append(":inbox_tray: Download Speed: ``" + str(st.download()) + "``")
        #lines.append(":outbox_tray: Upload Speed: ``" + str(st.upload()) + "``")
        #lines.append(":chart_with_upwards_trend: Ping: ``" + str(st.ping()) + "``")
        lines.append(":musical_note: Music Is Playing: ``" + str(self.bot.videoPlaying) + "``")
        lines.append(":control_knobs: Last Volume: ``" + str(self.bot.lastVolume) + "``")
        if not self.bot.ws is None: lines.append(":electric_plug: Web Socket: ``" + str(self.bot.ws) + "``")
        lines.append(":page_with_curl: Cached Messages Count: ``" + str(len(self.bot.cached_messages)) + "``")
        lines.append(":key: AppID: ``" + str(info.id) + "``")
        bigString = ("\n".join(lines))
        await ctx.send(bigString)



    @commands.command(pass_context=True, brief="HIDDEN", description="HIDDEN")
    async def permtest(self, ctx, role:str = "admin"):
        await self.bot.safe_delete(ctx.message)
        allowed, reason = (await self.bot.permissions_hasrole(self, ctx.message.author, role))
        if allowed:
            await ctx.send("Allowed: ``TRUE``, Reason: ``" + reason + "``")
            return

        else:
            await ctx.send("Allowed: ``FALSE``, Reason: ``" + reason + "``")
            return


    @commands.command(pass_context=True, brief="HIDDEN", description="HIDDEN")
    async def eval(self, ctx, *, cmd:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message) 

        current_milli_time = lambda: int(round(time.time() * 1000))
        start_milli_time = current_milli_time()

        if (cmd=="UNDEFINED"): cmd = 'await ctx.send(embed=(await bot.generate_error(self, "You should add the code you wish to run after the command. Like:\n``'+self.bot.config["prefix"]+'eval Cmd``'
        def insert_returns(body):
            # insert return stmt if the last expression is a expression statement
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])

            # for if statements, we insert returns into the body and the orelse
            if isinstance(body[-1], ast.If):
                insert_returns(body[-1].body)
                insert_returns(body[-1].orelse)

            # for with blocks, again we insert returns into the body
            if isinstance(body[-1], ast.With):
                insert_returns(body[-1].body)


        permCheck, err = (await self.bot.permissions_isowner(self, ctx.message.author))
        if permCheck:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"

            try:
                parsed = ast.parse(body)
            except Exception:
                trace = traceback.format_exc()
                trace = trace.replace("`", "")
                await ctx.send("You Entered:\n```" + cmd + "```")
                await ctx.send("\nError:\n```" + trace + "```")

            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'self': self,
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            if not result is None:
                if (str(self.bot.config["token"]).upper() in ((result.content).upper())):
                    await ctx.send(embed=(await self.bot.generate_error(self, "The result of the command you entered contains blocked data. For this reason the output has been stopped.")))
                    return

                else:
                    await ctx.send(result)
                    return

            else:
                await ctx.send(embed=(await self.bot.generate_error(self, f"Ran Successfully in {str(float(current_milli_time() - start_milli_time))} milliseconds")), delete_after=20)
                return

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
            return


def setup(bot):
    bot.add_cog(Utils(bot))