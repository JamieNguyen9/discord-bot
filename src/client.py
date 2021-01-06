import discord
from discord.ext.commands import Bot
import os
import command_helper
import random

BOT_PREFIX = '>'
BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

client = Bot(command_prefix=BOT_PREFIX)

# Runs when bot starts 
@client.event
async def on_ready():

    print('------')
    print(client.user.name + ' is now online.')
    print('')
    print('------')

# Process messages sent to chat
@client.event
async def on_message(message):
    await client.process_commands(message)


# Send random images of carl wheezer
@client.command(pass_context=True)
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
        await ctx.send("{}: Your dice rolls are: {}. Highest Value: {}.".format(ctx.message.author.mention, str(rolls), str(max_val)))
        return

    await ctx.send("{}: Your dice rolls are: {}.".format(ctx.message.author.mention, str(rolls)))
    return

client.run(BOT_TOKEN)