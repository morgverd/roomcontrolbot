import discord, asyncio
from discord.ext import commands
import urllib, random
import aiohttp
import pornhub
import requests, json, simplejson
from requests.utils import requote_uri

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def channel_is_blocked(self, ctx):
        # Not in NSFW channel
        await ctx.send(embed=(await self.bot.generate_error(self, (f":underage:  <@{ctx.message.author.id}> You must be in a NSFW channel to use this command!"))), delete_after=20)
        return

    async def getfromapi(self, ctx, url, contenttype, tags = "UNDEFINED"):
        data = None
        error = False
        try:
            url = requote_uri(url)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as responce:
                    if responce.status == 200:
                        data = (await responce.json(content_type=contenttype))
                    else:
                        error = True

        except simplejson.errors.JSONDecodeError:
            error = True

        if data == None: error = True
        if error:
            if not tags == "UNDEFINED":
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found for '||" + tags + "||'"), footer=f"From {ctx.message.author.name}")), delete_after=20)
            else:
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found."), footer=f"From {ctx.message.author.name}")), delete_after=20)
            return None

        return data


    @commands.command(pass_context=True, aliases=['34'], brief="*|cmd search|nsfw", description="Search Rule34 for any search term and then show it in the chat for all to see. (Some horrible things are on there, so be careful)")
    async def rule34(self, ctx, *, tags:str = "UNDEFINED"):
        await self.bot.safe_delete(ctx.message)
        if not ctx.message.channel.is_nsfw(): return await self.channel_is_blocked(ctx)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "canusensfw"))
        if permCheck:

            if (tags == "UNDEFINED"):
                await ctx.send(embed=(await self.bot.generate_error(self, "Incorrect usage. Please use ``"+self.bot.config["prefix"]+"rule34 searchterm``, replacing the searchterm with what you wish to say.\nFor example: ``"+self.bot.config["prefix"]+"rule34 undertale``")), delete_after=20)
                return
            await ctx.channel.trigger_typing()

            # Appologies
            weirdShit = [
                "PISS",
                "SHIT",
                "POO",
                "WEE",
                "SCAT",
                "CHILD",
                "FEET",
                "FECESE",
                "URINE"
            ]

            for bad in weirdShit:
                if bad.upper() in tags.upper():
                    try:
                        await ctx.message.author.kick(reason="Werido with 34 command")
                    except Exception:
                        pass
                    await ctx.send("Fuck off weirdo", delete_after=20)
                    return

            tags = tags.lower()
            url = ("http://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=500&tags={}".format(tags))
            data = await self.getfromapi(ctx, url, "text/html", tags=tags)
            if data is None: return
            try:
                count = len(data)
            except TypeError:
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found for (||" + tags + "||)"), footer=f"For {ctx.message.author.name}")), delete_after=20)
                return
            if count == 0:
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found for (||" + tags + "||)"), footer=f"For {ctx.message.author.name}")), delete_after=20)
                return
            image_count = 4
            if count < 4:
                image_count = count
            for i in range(count):
                image = data[random.randint(0, (count - 1))]
                imageURL = ("https://img.rule34.xxx/images/{}/{}".format(image["directory"], image["image"]))
                if (not (imageURL.endswith(".png"))) and (not (imageURL.endswith(".webm"))): break
            print("[PRON][RULE34] Got: " + imageURL)
            await ctx.send(embed=(await self.bot.generate_embed(self, title=("Rule 34 - " + tags), image=imageURL, footer=f"For {ctx.message.author.name}")), delete_after=20)
            return

        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return   

    @commands.command(pass_context=True, aliases=['yan'], brief="*|cmd|nsfw", description="Gets a random Yandere image. (Yandere is straight Hentai)")
    async def yandere(self, ctx):
        await self.bot.safe_delete(ctx.message)
        if not ctx.message.channel.is_nsfw(): return await self.channel_is_blocked(ctx)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "canusensfw"))
        if permCheck:
            await ctx.channel.trigger_typing()
            url = ("https://yande.re/post/index.json?limit=500")
            data = await self.getfromapi(ctx, url, "application/json")
            if data is None: return
            try:
                count = len(data)
            except TypeError:
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found."), footer=f"For {ctx.message.author.name}")), delete_after=20)
                return
            if count == 0:
                await ctx.send(embed=(await self.bot.generate_embed(self, title=("No results were found."), footer=f"For {ctx.message.author.name}")), delete_after=20)
                return
            image_count = 4
            if count < 4:
                image_count = count
            for i in range(count):
                imageURL = (data[random.randint(0, count)]["file_url"])
                if (not (imageURL.endswith(".png"))) and (not (imageURL.endswith(".webm"))): break
            print("[PRON][YANDERE] Got: " + imageURL)
            await ctx.send(embed=(await self.bot.generate_embed(self, title=("Yandere"), image=imageURL, footer=f"For {ctx.message.author.name}")), delete_after=20)
            return
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return   
    @commands.command(pass_context=True, brief="*|cmd|nsfw", description="Gets a random Yaoi image. (Yaoi is gay Hentai)")
    async def yaoi(self, ctx):

        await self.bot.safe_delete(ctx.message)

        if not ctx.message.channel.is_nsfw(): return await self.channel_is_blocked(ctx)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "canusensfw"))
        if permCheck:

            fp = urllib.request.urlopen("https://cdn.morgverd.xyz/pron/g.php")
            mybytes = fp.read()
            url = mybytes.decode("utf8")

            fp.close()
            embed=discord.Embed(title="For " + ctx.message.author.name, color=(await self.bot.generate_embedcolor()))
            embed.set_image(url=str(url))
            embed.set_footer(text="Will Self-Destruct in 20 seconds")
            await ctx.send(embed=embed, delete_after=20)
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return  

    @commands.command(pass_context=True, brief="*|cmd search|nsfw", description="Search PornHub for any search term and get the Thumbnail. It will even give you the URL if you'd like to do some... further research.")
    async def pornhub(self, ctx, *, searchTerm: str = "Sex"):
        
        await self.bot.safe_delete(ctx.message)

        if not ctx.message.channel.is_nsfw(): return await self.channel_is_blocked(ctx)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "canusensfw"))
        if permCheck:
            loadingMessage = await ctx.send(f"``Searching for {searchTerm}. Please wait...`` :hourglass_flowing_sand:")

            phClient = None; phURL = None
            phClient = pornhub.PornHub(list(searchTerm))
            phURL = ""

            videos = []
            for x in phClient.getVideos(100,page=1):
                videos.append(x)

            video = videos[random.randint(0, len(videos) - 1)]
            phURL = video["background"]

            embed=discord.Embed(title="For " + ctx.message.author.name + ". Search : " + searchTerm, color=(await self.bot.generate_embedcolor()))
            embed.set_image(url=str(phURL))
            embed.set_footer(text="Will Self-Destruct in 20 seconds")
            embed.add_field(name="URL", value=str(video["url"]), inline=False)
            await ctx.send(embed=embed, delete_after=20)
            try:
                await loadingMessage.delete()
            except Exception:
                pass
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return 

    @commands.command(pass_context=True, brief="*|cmd|nsfw", description="Gets a random image from e621 (Furry Porn)")
    async def e621(self, ctx):

        await self.bot.safe_delete(ctx.message)

        if not ctx.message.channel.is_nsfw(): return await self.channel_is_blocked(ctx)
        permCheck, err = (await self.bot.permissions_hasrole(self, ctx.message.author, "canusensfw"))
        if permCheck:
            
            fp = urllib.request.urlopen("https://cdn.morgverd.xyz/pron/t.php")
            mybytes = fp.read()
            url = mybytes.decode("utf8")

            fp.close()
            embed=discord.Embed(title="For " + ctx.message.author.name, color=(await self.bot.generate_embedcolor()))
            embed.set_image(url=str(url))
            embed.set_footer(text="Will Self-Destruct in 20 seconds")
            await ctx.send(embed=embed, delete_after=20)    
        else:
            await ctx.send(embed=(await self.bot.generate_error(self, err)))
        return 



def setup(bot):
    bot.add_cog(NSFW(bot))