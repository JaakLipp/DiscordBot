from ast import alias
import discord
from discord.ext import commands

'''
class containing all functions for displaying patch notes
'''
class patch_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.patch_notes = """
        ```
PATCH NOTES:
- !item gives an item for use in phasmophobia roulette        
        ```
        """
    '''
    command: patch
    output: an item to use in phasmophobia
    '''
    @commands.command(name='patch')
    async def patch(self, ctx):
        await ctx.send(self.patch_notes)

