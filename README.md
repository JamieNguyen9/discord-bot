# scraps-bot
A simple, multipurpose, Python-based Discord bot designed to handle a single Discord server.

## Features
* Youtube Music Player
* Dice Roller
* Carl Wheezer Random Image Generator
* Role Color Changer
* Real-time COVID Tracker
* Custom Twitter Tweet Tracker

## Prerequisites
The following dependencies are required for hosting your bot:
* tweepy (v3.10.0)
* discord.py (v1.5.1)
* youtube_dl (v2021.1.3)
* python (v3.8.7)
* FFmpeg (v3.4.8)

## Setup 
1. Clone the github repository to your coding environment
2. Install the dependencies as listed in the *Prerequisites* section. 
    * The method to install python and FFmpeg depends on the operating system. For bash, execute these commands
        ```bash
        $ sudo apt update
        $ sudo apt install python3.8
        $ sudo apt install ffmpeg
        ```
        For the rest of the dependencies, you would need to use `pip install ` as supplied by python
3. Create a [Discord](https://discord.com/developers/applications) and [Twitter developer](https://developer.twitter.com/en) account. Create applications on both developer accounts and keep note of their tokens for the next step.
4. Store these tokens as environment variables in your coding environment and name them the same as what is named in the source files (or rename the variables in the source file based on what you named your environment variables). 
5. You are now all set! See *Running the bot locally* to see how you can run the bot on your machine!

## Running the bot locally
1. Invite your bot to your discord server. [Here](https://discordpy.readthedocs.io/en/latest/discord.html) is how you would do it. 
2. Navigate to the /src folder on the cloned repo and run the *client.py* file.

## Hosting On the Cloud (Heroku - 24/7)
Watch this [video](https://youtu.be/wXn2iIGgHuU) on how to host your bot for free 24/7! 

Credits to Caleb Coffin for making this video.

## References
* [Discord.py Documentation](https://discordpy.readthedocs.io/en/latest/#)
* [Discord Developer Portal](https://discord.com/developers/)
* [Tweepy Documentation](https://docs.tweepy.org/en/latest/)
* [Heroku](https://www.heroku.com/)

## License
See the LICENSE File for more information.