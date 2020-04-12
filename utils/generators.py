
import asyncio, aiohttp, aiosocks, discord, async_timeout
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time, jsonpickle

class Generators():
    def __init__(self, bot, cursor):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def generate_embedcolor():
        colors = [
            0x009999, # teal
            0x0000ff, # blue
            0x6699ff, # light blue
            0x00cc66, # light green
            0x006600, # green
            0xffff66, # yellow
            0xff9900, # orange
            0xff6699, # pink
            0x993399, # dark purple
            0x9933ff #  purple
        ]
        color = colors[random.randint(0, (len(colors) - 1))] # Get random color
        return color



    async def generate_embed(self, title = "UNDEFINED", image = "UNDEFINED", subtitle = "UNDEFINED", text = "UNDEFINED", inline = False, footer = "UNDEFINED", author = "UNDEFINED"):
        embed = discord.Embed(title=title, color=(await self.bot.generate_embedcolor()))
        if not image=="UNDEFINED": embed.set_image(url=image)
        if not footer=="UNDEFINED": embed.set_footer(text=footer)
        if ((not (subtitle=="UNDEFINED")) and (not (text=="UNDEFINED"))): embed.add_field(name=subtitle, value=text, inline=inline)
        if not author=="UNDEFINED": embed.set_author(name=author)
        return embed

    async def generate_error(self, errorMessage):
        embed = discord.Embed(title="Error", color=0xFF0000, description=str(errorMessage))
        return embed