import discord
from discord.ext import commands

'''
Help Cog
Author: Jamie Nguyen

Provides help commands for every command in the bot.


'''

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help Cog has loaded.\n\n------')
    
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title = "Help",
            description = "Use the >help <command> for more information on that command",
            color = ctx.author.color
        )
        embed.add_field(name = "Music Bot Commands", value = "play, leave, queue", inline = False) 
        embed.add_field(name = "Role Command", value = "rolecolor", inline = False)
        embed.add_field(name = "Miscellaneous Commands", value = "covid, roll, carl, twitter_channel", inline = False)
        await ctx.send(embed = embed)
    
    @help.command()
    async def play(self, ctx):
        embed = discord.Embed(
            title = "Play",
            description = "Plays music from Youtube. If the music is currently playing, it adds the queried song to the queue.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">play <song name>")
        await ctx.send(embed = embed)

    @help.command()
    async def leave(self, ctx):
        embed = discord.Embed(
            title = "Leave",
            description = "Leaves the voice channel.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">leave")
        await ctx.send(embed = embed)

    @help.command()
    async def queue(self, ctx):
        embed = discord.Embed(
            title = "Queue",
            description = "Shows a list of songs next in queue.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">queue")
        await ctx.send(embed = embed)

    @help.command()
    async def rolecolor(self, ctx):
        embed = discord.Embed(
            title = "Role Color",
            description = "Changes the color (RGB value) of the role the user specifies if the user is in that role.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">rolecolor <role name> <R> <G> <B>")
        await ctx.send(embed = embed)

    @help.command()
    async def covid(self, ctx):
        embed = discord.Embed(
            title = "Covid",
            description = "Retrieves up-to-date coronavirus cases and deaths of the top 15 states in the US.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">covid")
        await ctx.send(embed = embed)

    @help.command()
    async def roll(self, ctx):
        embed = discord.Embed(
            title = "Roll",
            description = "Rolls an x amount of n-sided dice.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">roll <'xdn'>[Optional: add 'kh' to retrieve the highest roll from the rolls]")
        embed.add_field(name = "Variables", value = "x = number of rolls\nn = number of sides of the dice", inline = False)
        await ctx.send(embed = embed)

    @help.command()
    async def carl(self, ctx):
        embed = discord.Embed(
            title = "Carl",
            description = "Sends a random picture of carl wheezer",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">carl")
        await ctx.send(embed = embed)

    @help.command()
    async def twitter_channel(self, ctx):
        embed = discord.Embed(
            title = "Twitter_channel",
            description = "Changes the channel that twitter updates get sent to.",
            color = ctx.author.color
        )
        embed.add_field(name = "Syntax", value = ">twitter_channel <channel_id>")
        await ctx.send(embed = embed)