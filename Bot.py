import discord
from discord.ext import commands
import os

#import all of the cogs
from help_cog import help_cog
from music_cog import music_cog
from patch_cog import patch_cog

#set the command prefix
bot = commands.Bot(command_prefix='!')

#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot
bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(patch_cog(bot))

#start the bot with our token
token = ""
with open("token.txt") as file:
    token = file.read()

bot.run(token)



