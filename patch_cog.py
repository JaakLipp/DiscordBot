from ast import alias
import discord
from discord.ext import commands

class patch_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.patch_notes = """
        ```
        PATCH NOTES:
        
- Fixed a bug where skip would keep skipping
- Fixed a bug where some capitalizations would not work for commands
- Gabe can't play any version of thomas tha dank engine
- Fixed a bug where some songs wouldn't play due to restrictions
        ```
        """

    @commands.command(name='patch')
    async def patch(self, ctx):
        await ctx.send(self.patch_notes)

