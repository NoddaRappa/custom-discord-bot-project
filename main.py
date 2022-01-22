import discord
from discord.ext import commands
import dotenv
import os

import asyncio
import io
import aiohttp
from discord.ext.commands.errors import CommandInvokeError

import youtube_dl

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

ydtl_format_options = {
    'format': 'best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ydtl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get ('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

async def play_sound(ctx, url):
    author_voice_state = ctx.message.author.voice
    if not author_voice_state:
        await ctx.send('Please join a channel to use this command.')
        
    
    channel = author_voice_state.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild) #says bot object does not have client attribute.
    if voice:
        await voice.move_to(channel)
    else:
        await channel.connect()

    
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=ctx.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

bot = commands.Bot(command_prefix="!")

@bot.command()
async def shutup(ctx):
    """Plays the 'Did know know, that if you stop talking...' audio"""
    await play_sound(ctx, 'https://www.youtube.com/watch?v=wOf1RP4Cq4w')

@bot.command()
async def law(ctx):
    """Plays the 'Cool it with the anti-semitic remarks' clip from the film American Psycho (2000)"""
    await play_sound(ctx, 'https://www.youtube.com/watch?v=-cWipgJDEOA')

@bot.command()
async def battlepass(ctx):
    """Plays the 'that shit looks like the battle pass' video"""
    await play_sound(ctx, 'https://www.youtube.com/watch?v=6V0QQDuo26c')
    
@bot.command()
async def binted(ctx):
    """Plays Cave Noise 1 from Minecraft"""
    await play_sound(ctx, 'https://www.youtube.com/watch?v=_fGJxPbxYf0')

@bot.command()
async def yell(ctx):
    """Plays the audio of Tom from 'Tom and Jerry' yelling"""
    await play_sound(ctx, 'https://www.youtube.com/watch?v=eHSJeuD3HAM')

@bot.command()
async def join(ctx):
    """Makes the bot join voice"""
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()
    else:
        await ctx.send('Please join a channel to use this command.')

@bot.command()
async def leave(ctx): 
    """Makes the bot leave voice"""
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice:
        await voice.disconnect()
    else:
        await ctx.send('Bot not currently in voice channel.')
    

@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.id == bot.user.id:
        return
    elif after.channel and before.channel != after.channel:
        voice = after.channel.guild.voice_client
        time = 0
        while True:
            await asyncio.sleep(1)
            time += 1
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 20:
                await voice.disconnect()
            if not voice.is_connected():
                break

@bot.event
async def on_message(message):
    if "sus" in message.content.lower().split():
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tinyurl.com/ya83aknu') as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'JermaSus.png'))
    if message.content.lower() == "amogus":
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tinyurl.com/57h342aj') as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'amogus.png'))
    await bot.process_commands(message)




@bot.event
async def on_ready():
    print('Practice-bot is now online')

bot.run(TOKEN)