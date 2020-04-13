
import asyncio, aiohttp, aiosocks, discord, async_timeout
import os, sys, linecache, async_timeout, inspect, traceback
import re, math, random, uuid, time, jsonpickle
import pathlib

# Do not edit unless you have a good understanding of both Python and DiscordPY.
# Help: https://github.com/MorgVerd/roomcontrolbot/#hooks

class Hooks():
    def __init__(self, bot, cursor):
        self.bot = bot
    
    async def messageSent(bot, message):
        # Called whenever any message is sent
        # Could be in server or PMs. Any content type
        # Could even be the bots message

        # bot = Bot object
        # message = Message object sent by user
        return

    async def tokenExposed(bot, message):
        # Called when a message contains the bots token
        # Could be in server or PMs. Only text content

        # bot = Bot object
        # message = Message object sent by user
        return

    async def messageInPMs(bot, message):
        # Called when the bot is PMed a message and its not help command
        # Could be any content type

        # bot = Bot object
        # message = Message object sent by user
        return

    async def commandSent(bot, oldmessage, newmessage):
        # Called when a command is sent in the server and its a valid command
        # No permission checks preformed yet

        # bot = Bot object
        # oldmessage = Users original message object sent
        # newmessage = oldmessage with content modified to be lowercase, Actually ran
        return

    async def commandDoesntExist(bot, message, closestMatches):
        # Called when a user sends an incorrect command into the server

        # bot = Bot object
        # message = Message object sent by user
        # closestMatches = Array of closest commands to whats entered. Can be empty if it couldnt find one
        return

    async def standardMessage(bot, message):
        # Message is standard, Could be image etc. Isnt one of our commands anyway.

        # bot = Bot object
        # message = Message object sent by user
        return

    async def messageDeletedUserChatBanned(bot, message):
        # Message is going to be deleted since the user is chatbanned

        # bot = Bot object
        # message = Message object sent by user
        return

    async def presenceChangerUpdate(bot, mode, string):
        # Presence Changer has updated the status

        # bot = Bot object
        # mode = Always UPPER. Either PLAYING or WATCHING depending on type set
        # string = The status string
        return

    async def presenceChangerBlocked(bot):
        # Presence Changer status has been blocked as a song is playing
        # Since a song is playing the status should not be changed

        # bot = Bot object
        return

    async def disconnectEvent(bot):
        # on_disconnect triggered. Bot is about to autorestart

        # bot = Bot object
        return


    async def killMusic(bot):
    	# Any playing music is being killed

    	# bot = Bot object
    	return

    async def speaking(bot, raw, string):
    	# Bot is about to speak a message

    	# bot = Bot object
    	# raw = The message string sent by the user uncleaned
    	# string = The message string cleaned and used
    	return 