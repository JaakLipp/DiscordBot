import discord
from discord.ext import commands
import random

'''
For fun modifications of the game "Phasmophobia"
'''
class phasmo_cog(commands.Cog):

    def __init__(self, bot):
        self.list_of_items = ['Smudge Stick', 'Candle', 'EMF', 'UV', 'Motion Sensor', 'Tripod',
                              'Video Camera', 'Photo Camera', 'Sound sensor', 'Parabolic Microphone',
                              'Ghost Writing Book', 'Spirit Box', 'Glow Stick', 'DOTS', 'Salt',
                              'Sanity Pills', 'Thermometer', 'Crucifix']
        self.list_of_maps = ['Tanglewood', 'Ridgeview', 'Bleasdale', 'Edgefield', 'Grafton', 'Willow Street',
                             'Prison', 'Asylum', 'Brownstone', 'Maple Lodge']
        self.list_of_difficulties = ['Professional', 'Nightmare']

    '''
    Gets a random item from a list of items for a person to use in-game
    '''
    @commands.command(name='item')
    async def item(self, ctx, arg):

        for i in range(0,int(arg)):
            await ctx.send('-' + random.choice(self.list_of_items))


    '''
    Gets a random map to play on
    '''
    @commands.command(name='map')
    async def map(self, ctx):
        await ctx.send(random.choice(self.list_of_maps))

    '''
    Gets a random difficulty
    '''
    @commands.command(name='difficulty')
    async def difficulty(self, ctx):
        await ctx.send(random.choice(self.list_of_difficulties))
