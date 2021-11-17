
<p align="center">
    <img src = "readme-media/logo.png">
</p>

# Kakapo
Discord bot for the SESO discord

## Features
- Posts to the subreddit r/FindaUnit
- Provides moderation commands for admins
- Sends a welcome message to new users
- Supports YouTube video to audio/music streaming
- Applies a Tenor Gif Filter
- Provides miscellaneous commands for the users
- Supports the option to send a Reaction Roles message.
- Shiba...

## Commands
`!load <cogs name without .py from folder /cogs>`<br />
Load cog.

`!unload <cogs name without .py from folder /cogs>`<br />
Unload cog.

`!reload`<br />
Reloads all cogs

`!reload <cogs name without .py from folder /cogs>`<br />
Reloads a specific cog

`!version`<br />
Post the latest changes to the bot.

`!kill` **Debug**<br />
Kills the bot process. Useful for debugging.

`!ping`<br />
Pings the bot. Bot will pong back with latency.

`!play !P !p <YouTube URL>`<br />
Converts a YouTube video to audio then plays it in the user's voice channel.

`!skip`<br />
Skips the current video.

`!leave`<br />
Removes the bot from the current channel.

`!pause`<br />
Pauses the current playing video.

`!resume`<br />
Resumes the current playing video.

`!stop`<br />
Indefinitely stops the current video from playing. Unlike `!pause`, you cannot continue playing the current song. You can still use `!skip` and `!play` to continue with the rest of the queue.

`!queue`<br />
Display a queue of all videos to be played.

`!clear !Clear !Empty`<br />
Clear the queue of videos.

`!clean <integer>` **Admin**<br />
Removes a certain amount of messages.

`!ban @user` **Admin**<br />
Bans a user from the guild.

`!unban @user` **Admin**<br />
Unbans a user.

`!mute @user` **Admin**<br />
Mutes a user. This is persistent even if the user leaves and returns to the guild.

`!unmute @user` **Admin**<br />
Unmutes a user.

`!roleReactMessage`<br />
Set up a role selector message in the current channel

`!dog !doge !doggeg !shiba !shibainu`<br />
Posts a random Shiba Inu picture, courtesy of http://shibe.online/
Idea by Dallkori#3909

`!limit`<br/>
Limits the amount of people who can join the Voice Channel

`!lock`<br/>
Locks the current Voice Channel

`!unlock`<br/>
Unlocks the current Voice Channel

`!destroy`<br/>
Deletes the current Voice Channel

`!help`<br/>
provides the User with the purpose of different commands

`!ip`<br/>
Provides the IP to the Arma 3 server

`!time`<br/>
either provides the current time or a time conversion

`!modlist`<br/>
Points to the modlist channel

`!teamspeak`<br/>
Points to the teamspeak info channel

`!acre`<br/>
points to the Acre2 info channel

`!training`<br/>
points to the training documents and manuals

`!logo`<br/>
Points to where a user can find info on joining the Arma 3 unit

`!rules`<br/>
Points to where the user can find the rules to the discord and in game.

`!new`<br/>
Gives the user information regarding the Discord Server.

`!ping`<br/>
Gives the user the Latency of the bot.

`!8ball`<br/>
Magic 8ball

`!calculate`<br/>
Simple calculator

`!dice`<br/>
Rolls a die

## Installation
To install it, your system needs the following dependencies on your project. Most of them can be installed with `pip` or the Python package manager of choice. The exception is `ffmpeg` which must be installed on your host as the Python package for ffmpeg is too old.

### Dependencies
- Python 3.8
- `ffmpeg`
- `nextcord`
- `dotenv`
- `datetime`
- `youtube-search-python`
- `yt-dlp`

### Setup
Clone the project into a folder of your choice, enter it. In Unix it would be:

```shell
user@hostname:~ $ git clone https://github.com/Uncle-Sagbag/Kakapo.git
user@hostname:~ $ cd Kakapo
```

### Tokens
Tokens are sourced from `.env`. Create `.env` in the project folder.

```shell
user@hostname:~ $ nano .env
```

Paste the following tokens into your .env file. Feel free to change "example" to something else. Make sure you keep the quotation marks.

```
discord_token = "example"
user_agent = "example"
client_id = "example"
client_secret = "example"
redirect_uri = "example"
username = "example"
password = "example"
```

Press `CTRL+X` then `Y` to save the file.

### Execution
Running the bot is as simple as `python3 bot.py` inside the project folder. If that fails, make sure the tokens in .env are correct. If you want the bot to run in the background, install a package like `screen` or `termux` so there can be a terminal running in the background. Refer to those packages on how to set it up.

If you wish to post to FindAUnit, edit the `SESO.py` file to include your own recruitment message then run `python3 SESO.py`. To schedule this action, use crontab.

```shell
user@hostname:~ crontab -e
30 15 * * 1,3,5 /usr/bin/python3 /path/to/Kakapo/SESO.py >/dev/null 2>&1
```

This will run `python3 SESO.py` Monday, Wednesday, and Friday at 2:30 PM every day. Look into crontab editing if you wish to customize the timing. I use https://crontab-generator.org/ because I'm lazy :D