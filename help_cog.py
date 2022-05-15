from ast import alias
import discord
from discord.ext import commands

'''
Class containing all necessaryy functions to implement help function
'''
class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - Displays all the available commands
!item - Gets an item to use in Phasmophobia
!patch - Displays the latest patch notes
!play - Plays a song
!q - Displays the current music queue
!skip - Skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnects the bot from the voice channel
!pause - Pauses the current song being played or resumes if already paused
!resume - Resumes playing the current song
```
"""
        self.text_channel_list = []

    '''
    Command: help
    Output: All available commands of the bot
    '''
    @commands.command(name="help", aliases=['Help', 'HElp', 'HELp', 'HELP', 'HeLp', 'HelP', 'HeLP'], help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)



