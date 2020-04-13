import os, sys, random, time, datetime, subprocess, socket, json, io, textwrap, traceback, base64, contextlib, logging
import socket, errno

# Check versions
version = sys.version_info
if (not (version[0] == 3)): print("[FATAL] You must run on Python 3"); quit()
if (not (version[1] > 4)): print("[FATAL] You must run on Python 3.4+"); quit()
pythonVersion = str(str(version[0]) + "." + str(version[1]))

def safe_import(module, override=False, command="", install_name="", dont_print=False):
    attempts = 0

    while True:
        attempts += 1
        try:
            __import__(module)
            if not dont_print: print("[LAUNCHER] " + module + " imported")
            return
        except ImportError:
            if not override:
                if not dont_print: print(Fore.YELLOW + "[LAUNCHER][ERROR] " + module + " doesnt exist, Trying to install" + Style.RESET_ALL)

                if not install_name == "":
                    module = install_name
                os.system("python3 -m pip install " + module)
            else:
                if not dont_print: print(Fore.YELLOW + "[LAUNCHER][ERROR] " + module + " doesnt exist, Trying to install. Override on" + Style.RESET_ALL)
                os.system(command)

        if attempts > 5:
            if not dont_print: print(Fore.RED + "[LAUNCHER][FATAL] Tried to install " + module + " 5 times and failed each time. Exiting" + Style.RESET_ALL)
            quit()

# Make sure we have everything, If we dont install it
# Any new imports from any cogs go here

import pathlib, json
if not ((pathlib.Path("config.json")).exists()):
    if ((pathlib.Path("config.json.example")).exists()):
        print("[LAUNCHER][FATAL] Please rename 'config.json.example' to 'config.json' as outlined in the config guide here:\nhttps://github.com/morgverd/roomcontrolbot#configuration")
    else:
        print("[LAUNCHER][FATAL] Configuration file doesn't exist. Please follow the guide here:\nhttps://github.com/morgverd/roomcontrolbot#configuration")
    quit()
if not ((pathlib.Path("presences.py")).exists()):
    if ((pathlib.Path("presences.py.example")).exists()):
        print("[LAUNCHER][FATAL] Please rename 'presences.py.example' to 'presences.py.example' as outlined in the config guide here:\nhttps://github.com/morgverd/roomcontrolbot#configuration")
    else:
        print("[LAUNCHER][FATAL] Presences file doesn't exist. Please follow the guide here:\nhttps://github.com/morgverd/roomcontrolbot#configuration")
    quit()


with open("config.json", "r") as f:
    try:
        fileConfig = json.load(f)
    except json.decoder.JSONDecodeError as err:
        print("[LAUNCHER][FATAL] Configuration is not valid JSON. Are you missing any characters? Heres a helpfull message:\n" + str(err))
        quit()

currentDir = str(fileConfig["rootpath"])

if (not (fileConfig["skipsafeimports"] == "TRUE")):
    print("[LAUNCHER] Doing Imports")

    safe_import("colorama", dont_print=True); import colorama; from colorama import Fore, Style
    safe_import("discord", install_name="discord.py")
    safe_import("asyncio")
    safe_import("pathlib")
    safe_import("json_pickle", install_name="jsonpickle")
    safe_import("urllib.request")
    safe_import("dhooks")
    safe_import("aiohttp")
    safe_import("pytz")
    safe_import("googletrans")
    safe_import("inspect")
    safe_import("lxml")
    safe_import("PIL", install_name="pillow")
    safe_import("urbandict")
    safe_import("bs4", override=True, command="sudo apt-get install python3-bs4")
    safe_import("requests")
    safe_import("numpy")
    safe_import("pornhub", override=True, command=f"sudo apt-get install git && sudo rm -r {currentDir}/pornhub-api || true && sudo git clone https://github.com/sskender/pornhub-api && sudo mv {currentDir}/pornhub-api/pornhub /usr/lib/python{pythonVersion}/pornhub")
    safe_import("aiosocks")
    safe_import("difflib")
    safe_import("gtts", install_name="gTTs")
    safe_import("ast")
    safe_import("pytube", install_name="pytube3")
    safe_import("pysubs2")
    safe_import("pyspeedtest")
    safe_import("alsaaudio", override=True, command="sudo apt-get install python-alsaaudio")
    
else:
    import colorama; from colorama import Fore, Style
    print("[LAUNCHER][CONFIG] Skipped import checks")


from utils.funcs import Funcs
from utils.generators import Generators
from utils.permissions import Permissions
from utils.filters import Filters
from utils.hooks import Hooks
import difflib
from discord.ext import commands
import discord, asyncio

print("[LAUNCHER][CONFIG] Got prefix: '" + fileConfig["prefix"] + "'")

bot = commands.Bot(command_prefix=fileConfig["prefix"], description="A bot I use to inact my ausitic rage")
bot.remove_command("help") # Remove the Help command to be set by our own one later

# Get file configuration and load into bot.config so it can be ran as bot.config["arg"]

bot.config = fileConfig

# Funcs defintion
bot.funcs = Funcs
bot.get_json = Funcs.get_json
bot.get_text = Funcs.get_text
bot.safe_delete = Funcs.safe_delete
bot.killmusic = Funcs.killmusic
bot.read_raw = Funcs.read_raw
bot.speak = Funcs.speak
bot.cleanString = Funcs.cleanString

bot.hook = Hooks

# Generators defintion
bot.generators = Generators
bot.generate_embed = Generators.generate_embed
bot.generate_error = Generators.generate_error
bot.generate_embedcolor = Generators.generate_embedcolor

# Permission Manager
bot.permissions = Permissions
bot.permissions_isowner = Permissions.permissions_isowner
bot.permissions_hasrole = Permissions.permissions_hasrole
bot.permissions_isallowed = Permissions.permissions_isallowed
bot.permissions_userchatmuted = Permissions.permissions_userchatmuted
bot.permissions_userlivebanned = Permissions.permissions_userlivebanned

# Filter Manager
bot.filter_check = Filters.filter_check
bot.filter_englishonly = Filters.filter_englishonly

bot.commandnames = None # For message error detecton
bot.blacklistedwords = []
bot.videoData = {}
bot.videoPlaying = False
bot.videoCurrentTimer = 0
bot.lastVolume = 0
bot.ismuted = False
bot.subtitlesexist = False
bot.header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
bot.commandsCache = []

bot.bannedFromChannels = []
bot.bannedFromChannelID = {}


os.system("sudo killall vlc") # VLC Player for music
os.system("sudo killall php") # Stop any running webserver

"""
# Setup web
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((fileConfig["web"]["localIP"], int(fileConfig["web"]["port"])))
except socket.error as e:
    if e.errno == errno.EADDRINUSE:
        print("[FATAL][WEB] Port " + fileConfig["web"]["port"] + " is in use, Please change in config")
    else:
        print("[FATAL][WEB] " + str(e))
    quit()
s.close()
os.system("lxterminal -e sudo php -S " + bot.config["web"]["localIP"] + ":" + bot.config["web"]["port"] + " -t " + bot.config["rootpath"] + "/web")
"""

os.system("lxterminal -e amixer set PCM -- 0%") # Set to default
print("[LAUNCHER] Set volume to 0%")

async def checkServerConnections():
    for server in bot.guilds:
        if not (int(server.id) == (bot.config["serverID"])):
            print("[LAUNCHER] Bot is in " + str(server.name) + " (" + str(server.id) + "). This is not the serverID listed in Config.py. About to leave")
            try:
                await server.leave()
                print("[LAUNCHER] Successfully left " + str(server.name) + " (" + str(server.id) + ")")
            except Exception:
                print(Fore.YELLOW + "[LAUNCHER][ERROR] Couldn't leave " + str(server.name) + " (" + str(server.id) + ")" + Style.RESET_ALL)
    return

@bot.event
async def on_ready():
    print("[LAUNCHER] on_ready() triggered. Bot active.")
    print("[LAUNCHER] Checking for server connections.")
    await checkServerConnections()
    print(Fore.GREEN + "[LAUNCHER] Finished lancher." + Style.RESET_ALL)
    await bot.change_presence(activity=discord.Game(name='Initialising Bot...'))
    await bot.speak(bot, "Initialising", isbot=True)

@bot.event
async def on_message(message):
    await bot.hook.messageSent(bot, message)
    if (((bot.config["token"]).upper()) in ((message.content).upper())):
        await bot.hook.tokenSent(bot, message)
        print(Fore.YELLOW + "[LAUNCHER][WARNING] Token was mentioned in chat, Removing it" + Style.RESET_ALL)
        # Token is in message
        await bot.safe_delete(message)
        await message.channel.send(embed=(await bot.generate_error(message, f"The message sent by <@{message.author.id}> contains content that we consider to be sensitive. For this reason message was deleted.")), delete_after=20)
        return
    # Do a few checks
    if (bot.commandnames == None):
        cmds = (bot.commands)
        bot.commandsCache = cmds
        cmdList = []
        for cmd in cmds:
            cmdList.append((cmd.name).upper())
            if not (len(cmd.aliases) == 0):
                for alias in (cmd.aliases):
                    # alias's
                    cmdList.append(alias.upper())

        bot.commandnames = cmdList
        print("[LAUNCHER] Initialised Command Error detection.")

    if message.author.id == bot.user.id: return
    if ((message.content).startswith(bot.config["prefix"])):

        strip_a = str(message.content).replace(bot.config["prefix"], "")
        if " " in strip_a:
            strip_b = (strip_a.split(" "))[0]
        else:
            strip_b = strip_a
        strip_b = strip_b.replace(" ", "")
    if message.guild is None:
        # In PM's
        if ((strip_b.upper()) == "HELP"):
            await bot.process_commands(message) # If its help
            return
        await bot.hook.messageInPMs(bot, message)
        await message.channel.send("Well. :eyes:  We aren't in a Discord Server! Im an exclusive guy. If you want me please talk to me in a Discord Server. I dont do PM's :rolling_eyes:")
        return
    else:

        if ((message.content).startswith(bot.config["prefix"])):
            if ((str(strip_b).upper()) == "HELP"):
                await message.channel.send(embed=(await bot.generate_error(bot, "Please run this command in our PM's, Since everyone's help commands are tailored to them.")), delete_after=20)
                return
            if ((str(strip_b).upper()) in (bot.commandnames)):
                # command exists, Its a cmd
                print(Fore.MAGENTA + "[LAUNCHER][COMMAND RAN] " + str(message.author.name) + " (" + str(message.author.id) + ")  ->  " + (str((message.content).lower()).replace(bot.config["prefix"], "")) + Style.RESET_ALL)

                chars = (bot.config["prefix"] + (strip_b.lower()))
                charx = len(chars)
                fixedList = []
                for letter in list(chars):
                    fixedList.append(letter)

                i = 0
                for letter in (message.content):
                    if i >= charx: fixedList.append(letter)
                    i += 1

                fixedString = ("".join(fixedList))
                oldmessage = message
                message.content = fixedString # Replace content with Fixed string
                await bot.hook.commandSent(bot, oldmessage, message)
                await bot.process_commands(message)
                return

            await bot.safe_delete(message)

            cmd = (((message.content).replace(bot.config["token"], "")).replace(" ", "")).upper()
            if (len(cmd) == 0): cmd = "Nothing..."
            closestMatches = (difflib.get_close_matches(cmd, bot.commandnames))
            closestMatchString = ""
            if (len(closestMatches) == 0):
                closestMatchString = "There are no predictive closest matches found"
            else:
                closestMatchString = "The closest match to what you entered is ``" + str(closestMatches[0]).lower() + "``. Did you mean that?"
            await bot.hook.commandDoesntExist(bot, message, closestMatches)
            embed=discord.Embed(title="Couldn't find that command")
            embed.set_footer(text="Will Self-Destruct in 20 seconds")
            embed.add_field(name="You Entered", value=("``"+str(cmd.lower())+"``"), inline=True)
            embed.add_field(name="Closest Match", value=str(closestMatchString), inline=False)
            await message.channel.send(embed=embed, delete_after=20)
            return
        
        else:
            # Not a command, Normal chat message.
            # Check if user is muted or not
            await bot.hook.standardMessage(bot, message)
            if (await bot.permissions_userchatmuted(bot, message.author, takeBot=True)):
                await bot.hook.messageDeletedUserChatBanned(bot, message)
                await bot.safe_delete(message)
                return

        return

async def presence_changer():
    print("[LAUNCHER] Loading presence_changer()")
    await bot.wait_until_ready()
    await asyncio.sleep(5)
    await bot.speak(bot, "Ready", isbot=True)
    usedIDs = []

    import presences
    listOfpresences = presences.listOfPrecences
    lengthOfpresences = 0
    for item in listOfpresences.values():
        lengthOfpresences += 1

    while True:

        if not (bot.videoPlaying):
            
            foundItem = False
            while (not foundItem):

                # Select an item
                if (len(usedIDs) == lengthOfpresences):
                    # Fucking shit has hit the wall. Panic
                    usedIDs = []

                i = random.randint(0, lengthOfpresences - 1)

                if (not (str(i) in usedIDs)):
                    usedIDs.append(str(i))
                    foundItem = True
                    string = list(listOfpresences)[i]; mode = listOfpresences[list(listOfpresences)[i]]
                    break
            
            if mode.upper() == "PLAYING":
                print("[LAUNCHER] Setting presence to 'PLAYING' '" + string + "'")
                await bot.change_presence(activity=discord.Game(name=string))
            elif mode.upper() == "WATCHING":
                print("[LAUNCHER] Setting presence to 'WATCHING' '" + string + "'")
                activity = discord.Activity(name=string, type=discord.ActivityType.watching)
                await bot.change_presence(activity=activity)
            else:
                print(Fore.RED + "[LAUNCHER][ERROR] Couldn't find valid dict item to change presence. Staying the same for now." + Style.RESET_ALL)

            await bot.hook.presenceChangerUpdate(bot, (mode.upper()), string)

            await asyncio.sleep(30)

        else:
            # Playing something, Wait
            await bot.hook.presenceChangerBlocked(bot)
            await asyncio.sleep(1)

@bot.event
async def on_disconnect():
    await bot.hook.disconnectEvent(bot)
    print(Fore.RED + "[LAUNCHER][DISCONNECT] Bot application is quitting" + Style.RESET_ALL)
    if bot.videoPlaying:
        # Video is playing
        os.system("killall vlc")
        bot.videoPlaying = False

    channel = bot.get_channel(bot.config["debugChannel"])
    print(Fore.GREEN + "[LAUNCHER][RELAUNCH] Attempting to begin relaunch..." + Style.RESET_ALL)
    os.system("python3 bot.py")

# Check needed for Vote Command in Fun
@bot.event
async def on_voice_state_update(member, before, after):
    if str(member.id) in bot.bannedFromChannels:
        # User is banned from channels still
        channelTheirBannedFrom = bot.bannedFromChannelID[str(member.id)]
        if (channelTheirBannedFrom == str(after.channel.id)):
            # User is not allowed there
            try:
                await member.send("You're still banned from going in there since people voted to have you removed. Try in ``5`` minutes time.")
            except Exception:
                pass

            channel = bot.get_channel(bot.config["afkvoice_channel"])
            try:
                await member.move_to(channel, reason=f"Tried to rejoin despite being votebanned")
            except Exception:
                pass
    return

if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            do = True
            if (str(filename[:-3]).upper() == "NSFW"):
                # Check NSFW config
                if not ((bot.config["allowNSFWcommands"]) == "TRUE"):
                    print("[LAUNCHER] NSFW Commands have been disabled. Not loading cog.")
                    do = False
            if do:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"[LAUNCHER][INFO] Loaded Cog : {filename[:-3]}")


presence_changer_task = bot.loop.create_task(presence_changer())
bot.run(bot.config["token"])