import discord, tweepy, asyncio
from discord.ext.commands import Bot
from discord.utils import get
from discord import FFmpegPCMAudio
import os, random, ctypes, ctypes.util
import command_helper, covid_helper, twitter_listener, help

'''
Discord Bot
Author: Jamie Nguyen

This is the file you run to get your bot up and running online. The heart of the bot. 

'''


BOT_PREFIX = '>'
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

client = Bot(command_prefix=BOT_PREFIX, help_command = None)
client.add_cog(help.Help(client))

song_queue = []
loop = asyncio.get_event_loop()

# Runs when bot starts 
@client.event
async def on_ready():
    # Initialization Stage
    print('------')
    print(client.user.name + ' is now online.')
    print('')

    # Setting up twitter listener
    twitter_api = twitter_listener.create_api()
    twitter_stream = tweepy.Stream(
        auth = twitter_api.auth,
        listener = twitter_listener.TweetListener(d_msg = send_tweet, loop = loop)
    )
    twitter_stream.filter(follow=['978760100977500161'], is_async=True)


# Process messages sent to chat
@client.event
async def on_message(message):
    await client.process_commands(message)


# Retrieves real time covid statistics from public api
@client.command()
async def covid(ctx):
    stats = covid_helper.get_covid_json()
    us = covid_helper.get_covid_us_json()
    embed = discord.Embed(
        title = "Coronavirus Statistics",
        description = "-----= U.S. Totals =-----\nCases: {:,}\nDeaths: {:,}".format(us[0]['positive'], us[0]['death']),
        colour = discord.Color.red()
    )
    states = covid_helper.get_states()

    numbered = 1
    for i in stats:
        header1 = "**{}. {}**".format(numbered, states[i['state']])
        val = "Cases: {:,}\nDeaths: {:,}".format(int(i['positive']), int(i['death']))
        embed.add_field(name = header1, value = val, inline=True)
        numbered += 1

    await ctx.send(embed = embed)
    

# Shows a list of songs next in queue
@client.command()
async def queue(ctx):
    embed = discord.Embed(
        title = 'Next song(s):',
        colour = discord.Color.red()
    )

    if len(song_queue) == 0:
        embed.add_field(name = 'None queued.', value = 'Feel free to add a song to the queue!')
        await ctx.send(embed = embed)
    else:
        numbered = 1
        for song in song_queue:
            embed.add_field(name = f"{str(numbered)}. **{song['title']}**", value = "\u200b", inline = False)
            numbered += 1
        await ctx.send(embed = embed)


# Plays a youtube video in voice channel
@client.command()
async def play(ctx, *, arg):
    channel = ctx.message.author.voice
    if channel:
        # if bot is not connected to voice
        if not client.voice_clients:
            await channel.channel.connect()
        
        # music set up
        voice = get(client.voice_clients, guild = ctx.guild)
        ctp = ctypes.util.find_library('opus')
        discord.opus.load_opus(ctp)

        # add song to queue
        song = command_helper.get_link(arg)
        song_queue.append(song)

        if not voice.is_playing():
            embed = discord.Embed(
                description = f"Now Playing: **{song_queue[0]['title']}**",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
            voice.play(FFmpegPCMAudio(song_queue.pop(0)['source'], **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
        else:
            embed = discord.Embed(
                description = f"Added to queue: **{song['title']}** [{ctx.message.author.mention}]",
                color = discord.Color.red()
            )
            await ctx.send(embed = embed)
    else:
        await ctx.send("You are not connected to a voice channel.")
        return


# Plays the next song after current song has finished playing
def play_next(ctx):
    voice = get(client.voice_clients, guild = ctx.guild)
    if len(song_queue) != 0:
        future = asyncio.run_coroutine_threadsafe(msg_title(ctx), loop)
        future.result()
        future.cancel()
        voice.play(FFmpegPCMAudio(song_queue.pop(0)['source'], **FFMPEG_OPTIONS), after = lambda e: play_next(ctx))
    else:
        future = asyncio.run_coroutine_threadsafe(leave(ctx), loop)
        future.result()
        future.cancel()


# Helper function for play_next()
async def msg_title(ctx):
    embed = discord.Embed(
        title = f"Now Playing: {song_queue[0]['title']}",
        color = discord.Color.red()
    )
    await ctx.send(embed = embed)


# Disconnects from voice channel
@client.command()
async def leave(ctx):
    song_queue.clear()
    await ctx.voice_client.disconnect()
    

@client.command()
async def skip(ctx):
    if not client.voice_clients:
        await ctx.send("The bot is not playing any music! Use `>play <song name>` to play music.")
    elif len(song_queue) == 0:
        await ctx.send("No songs left after this song. Use `>play <song name>` to add to the queue!")
    else:
        voice = get(client.voice_clients, guild = ctx.guild)
        voice.stop()
        

# Changes role color if user is in that role.    
@client.command()
async def rolecolor(ctx, role: str, r: int, g: int, b: int):
    # role is case sensitive
    if not command_helper.verify_role(role, ctx.message.author.roles):
        await ctx.send("You are not in {}. Please try again".format(role))
        return

    guild_role = discord.utils.get(ctx.guild.roles, name = role)
    await guild_role.edit(colour=discord.Color.from_rgb(r, g, b))
    await ctx.send("{}: {}'s color has now changed.".format(ctx.message.author.mention, role))


# Send random images of carl wheezer
@client.command()
async def carl(ctx):
    image = command_helper.get_carl()
    await ctx.send(image) 


# Perform x amount of y-dice roles in the format of "xdy"
# where x and y are positive integers
@client.command()
async def roll(ctx, arg: str):
    xdy = arg
    kh = False  # keep highest

    if xdy[-2:] == 'kh':
        kh = True
        xdy = xdy[:-2]

    rolls = command_helper.get_rolls(xdy)
    if isinstance(rolls, bool):
        await ctx.send("Argument is missing or is in the wrong format. Please try again")
        return

    if kh:
        max_val = max(rolls)
        await ctx.send("{}: Your dice rolls are: **{}**. Highest Value: {}.".format(ctx.message.author.mention, str(rolls), str(max_val)))
        return

    await ctx.send("{}: Your dice rolls are: {}.".format(ctx.message.author.mention, str(rolls)))
    return


# Changes where the bot sends the tweets
@client.command()
async def twitter_channel(ctx, id):
    command_helper.change_tw_id(int(id))


# Helper method to send real time tweet updates from a twitter account to a specific channel
async def send_tweet(json_msg):
    embed = discord.Embed(
        description = json_msg["text"],
        colour = discord.Color.blue()
    )
    embed.set_author(name = f'{json_msg["user"]["name"]} (@{json_msg["user"]["screen_name"]})', icon_url=json_msg["user"]["profile_image_url_https"])
    embed.set_footer(text = f'Twitter - {command_helper.convert_date(json_msg["created_at"])}', icon_url = command_helper.twitter_icon)
    await client.get_channel(command_helper.tweet_channel).send(embed = embed)


client.run(BOT_TOKEN)