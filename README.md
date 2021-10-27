
<p align="center">
    <img src = "readme-media/logo.png">
</p>

# Kakapo
Discord bot for the SESO discord

## Features
- Posts to the subreddit r/FindaUnit
- Provides moderation commands for admins
- Welcome message
- Supports YouTube video to audio streaming

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

## Installation
To install it, your system needs the following dependencies on your project.

### Dependencies
- `youtube-dl`
- `ffmpeg`
- `discord.py`

### Tokens
Tokens are sourced from `.env`. Create `.env` in the project folder with the following content:

#### Discord Token
```
discord_token = "example"
```
#### Reddit Tokens
```
user_agent = "example"
client_id = "example"
client_secret = "example"
redirect_uri = "example"
username = "example"
password = "example"
```
