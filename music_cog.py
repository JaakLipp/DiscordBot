from ast import alias
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

'''
class containing all necessary functions for various music-playing 
'''
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    # Helper function
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                # in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

     '''
     Command: play
     output: bot joins user's channel and plays specified song
     '''
    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args) + ' youtube audio'

        if str(ctx.channel) != 'music':
            await ctx.send("use the music chat idiot")
            return
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:

                await ctx.send('Now Playing: ' + song.get('title'))

                self.music_queue.append([song, ctx.author.voice.channel])

                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    '''
    command: pause
    output: pauses the current song playing or resumes a paused song
    '''
    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Paused")
        elif self.is_paused:
            self.vc.resume()
    
    '''
    command: resume
    output: resumes the curret song that is paused
    '''
    @commands.command(name="resume", aliases=['Resume', 'R,' 'r'], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

    '''
    command: skip
    output: skips the current song playing or displays a message saying there is nothing to skip
    '''
    @commands.command(name="skip", aliases=["s", 'S', 'Skip'], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None:
            self.vc.stop()
            # try to play next in the queue if it exists
            await self.play_music(ctx)
        else:
            await ctx.send("There is nothing to skip!")
    '''
    command: queue
    output: displays the music queue
    '''
    @commands.command(name="queue", aliases=["q", 'Q'], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
            
    '''
    command: clear
    output: skips the current song playing and clears the entire queue
    '''
    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")
        
    '''
    command: leave
    output: disconnects the bot from the voice channel
    '''
    @commands.command(name="leave", aliases=["disconnect", "l", "d", 'dc'], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
