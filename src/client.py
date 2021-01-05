import discord
from discord.ext.commands import Bot
import os
import carl_images
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
    image = carl_images.get_carl()
    await ctx.send(image) 

# Perform x amount of y-dice roles in the format of "xdy"
# where x and y are positive integers
@client.command()
async def roll(ctx, arg:str):
    i = 0
    j = 0
    args = []
    for c in arg:
        print(c)
        if c == 'd':
            args.append(int(arg[i:j]))
            i = j + 1
            j = i
            print(args)
        else:
            j += 1

    if j == i:
        await ctx.send("Arg is in the wrong format (needs to be in 'xdy' form). Please try again")
        return
    else:
        args.append(int(arg[i:j]))

    rolls = []
    for c2 in range(args[0]):
        rolls.append(random.randint(1, args[-1]))

    await ctx.send("Your dice rolls are: " + str(rolls))
    return

client.run(BOT_TOKEN)