<p align="center">
  <img width="740" height="160" src="https://cdn.morgverd.com/images/github/roomcontrolbot/logo.png" alt="Room Control Logo">
  <!--
    New Icon from shockingly enough, My new website CDN system!
  -->
</p>
<h2 align="center"><i>An Abomination to Discord Bots</i></h2><br>

This discord bot controls your PI3 and enables it to play music through a YouTube based search system and a text to speech system that allows users that you give a role to access to speak in your room.
\
This was never a serious project, just a fun thing do to.
## Features
- Sound commands, Allowing select users to speak and even play music in your room.
- Music search features allowing users to play songs based upon the name alone.
- Lyric command that gets the captions of the song (*If there is any*)
- Volume control for administrators to easily make any song louder or quieter.
- Now Playing command to allow you to see what is playing and points of data about the song.
- Automatic Age-restriction checks on songs.
- Automatic music length limiter.
- Fun commands that allow users to get pictures, define Urban Dictionary words, and more.
- Useful admin commands that allow your staff to safely control the server with ease.
- Extensive Filtering to block people from saying naughty things in  your room (*However, you can bypass this*)
- Optional range of NSFW commands.
- Easy to add your own commands and edit how the bot works.
## Installation

First, you must install the zip file. You will need to run:
```git
git clone https://github.com/MorgVerd/roomcontrolbot.git
```
Then, you will need to run:
```shell
unzip roomcontrolbot-master.zip 
```
### Dependencies 
One core requirement of the library that we use ([discord.py](https://github.com/Rapptz/discord.py)) is a version of Python installed that must be at least ``Version 3.4+`` to function correctly. If you attempt to use any other version of Python the script will automatically stop its-self.
\
The room control bot will automatically detect any missing PIP3 packages and will issue the needed commands to install them. However, You will need to install the following non-python packages:

- VLC
- Alsa-Utils
- PHP *(7.2+)*

To install the packages please run the following:
```bash
sudo apt-get install vlc
sudo apt-get install alsa-utils
sudo apt-get install php
```
## Configuration
First, rename ``config.json.example`` to ``config.json``. Then, You should rename ``presences.example.py`` to ``presences.py`` and open it up to configure it. The configuration should be explained inside. Inside the ``config.json`` these are the base settings.


``token`` = The Token given to you from [here](https://discordapp.com/developers/applications/).
\
``prefix`` = A one word prefix that the bot should use. Example: ``>>``, So command usage would be ``>>help``.
\
``skipsafeimports`` = **``TRUE`` or ``FALSE``, Should remain FALSE, This should only be ran if the launcher is trying to install things it already has**.
\
``ownerID`` = Your Discord user ID.
\
``serverID`` = Your Discord server ID.
\
``afkvoice_channel`` = The ID of your AFK Voice channel.
\
``debugChannel`` = The ID of the channel used to post Disconnect messages.
\
``muteassignrole`` = Should a role be given to muted people, If ``FALSE`` it will just remove any messages from muted people.
\
``requireNSFWrole`` = Should a role be required to use NSFW commands?
\
\
``roleIDs``
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``admin`` = The ID of the Administrator role that has access to Admin commands, and bypasses for Say command etc.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``music`` = The ID of the role that can use the ``play`` command.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``canusebot`` = The ID of the role that can use the Bot interactive commands as a whole. Base role.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``bypassmusiclimit`` = Can skip the maximum of 5 minute song length on the ``play`` command.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``canusensfw`` = Can use NSFW commands in NSFW channels.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``mutedrole`` = Role to give muted people if ``muteassignrole`` is ``TRUE``
\
\
``allowedtimes``
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``minimumtime`` = The 24 hour time of the EARLIEST time a command can be ran, *DEFAULT: 12*.
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``maximumtime`` = The 24 hour time of the LATEST time a command can be ran, *DEFUALT: 21 (9pm)*.
\
\
``web``
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``enabled`` = Is the web system enabled?
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``localIP`` = What is your local IP address for the PI being used? Eg: 192.168.?.??
\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``port`` = What port number should be used?
\
\
``rootpath`` = The root location of where the bot.py folder is. **There should not be any ending ``/``**.
\
``apiKey`` = Used to access the ``morgverd.xyz`` API services.
\
``allowNSFWcommands`` = ``TRUE`` or ``FALSE``. Turns on or off the NSFW commands. *DEFUALT: TRUE*

[How to get IDs](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
## Usage
To start the bot please run the following command:
```bash
python3 bot.py
```
The bot may take upto 5 minutes on its first load as it installs any missing dependancies automatically.

## Making Changes
One important thing to remember if you want to add your own commands to the bot.

Another is that you should not edit any of the following unless you have an understanding of both Python and DiscordPY rewrite branch. If you experience any issues editing or adding to the bots code I can not be expected to provide support etc.


Always use ``safe_delete()`` to remove messages instead of the standard ``delete_message``
```python
await self.bot.safe_delete(ctx.message) # Delete the command message
```
\
Another important thing to remember is to add any new commands to their own Cog.
\
To add a new Cog, First navigate to the ``cogs/`` folder and make a new python file, naming it anything. For this example we use ``example.py``
\
In ``example.py`` add the following:
```python

# First import all the default packages.
import discord, asyncio
from discord.ext import commands
from utils.generators import Generators
from utils.permissions import Permissions
from utils.funcs import Funcs
from utils.filters import Filters

# Change Example to whatever your Cog file is called
class Example(commands.Cog):
    # Copy exactly
    def __init__(self, bot):
        self.bot = bot
        # You can also define any other variables or functions you wish to use a lot here

    # Add command here (see example below for help)


def setup(bot):
    # Like above, Change Example to the name of your Cog
    bot.add_cog(Example(bot))

```
### Example command with Comments explaining usage cases :
```python
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
```

### Hooks
There a range of hooks you can edit to execute actions when something happens. You can find all of these in ``utils/hooks.py``. Inside you will see a range of functions with alot of comments. It is important that you **do not edit any of the function names in this file**. This is because the bot relies on calling the functions with its exact name.

At the end of any hook function you should always include ``return`` at the end. This is just to keep a neat code standard and to ensure that the bot knows that the function is closed.

### Defining your own config
\
You may be in a situation where you decide to add your own Configuration options. For this you simply add your configuration option to the ``config.json`` file and check its value using:
```python
print(self.bot.config["yourConfigOptionName"])
```
For example:
``config.json`` line added:
```json
    "amICool" : "YES",
```
``test.py`` cog line added:
```python
print(self.bot.config["amICool"])
```
Output:
```shell
>> YES
```
### Custom Import Packages
\
To import new packages in your Cogs, Please goto ``bot.py`` and add ``safe_import()`` function relating to the package.
\
Example usages (in ``bot.py``):
```python

# If the name of the PIP install command is the same as the package
safe_import("package")
import package

# If the name of the PIP install command is not the same as the package
safe_import("package", install_name="package-example") # This will import 'package' but download 'package-example'
import package

# If you have to use apt-get and not pip
safe_import("package", override=True, command="sudo apt-get install python-package")
import package


# One important thing to remember, Is not to use safe_import() as an actual importer. All it does is checks if it exists and downloads it if it dosent. You should still import tha package seperately after running this command.
# Since bot.py is ran first, This will install any packages needed then load Cogs, So you can put new packages in your Cog without downloading them first aslong as you define them here.
```
## Todo
I want to soon completely overhaul the Permissions System to allow for each role to have an assosiated weight, This should fix issues with users needing hyper specific roles to do certain things.
## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
