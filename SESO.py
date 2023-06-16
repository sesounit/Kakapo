import praw, os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(user_agent= os.getenv("user_agent"),
		  client_id= os.getenv("client_id"),
		  client_secret= os.getenv("client_secret"),
		  redirect_uri= os.getenv("redirect_uri"),
		  username= os.getenv("username"),
		  password= os.getenv("password"))

print(reddit.user.me())


s = """
# Variety with Common Sense Realism
SESO was established in 2018 as a unit focused on immersion, variety, and common sense realism for a complete Arma 3 experience. We design operations that are fun to play, easy to join, and asks as little as possible from you. Our casual playstyle is tailored towards having fun, but we always play to complete the objective. There is no required experience, minimum age, DLCs, or “basic training” in order to participate in our operations.

***
## Schedule
We focus on on EST (Eastern United States) timezone. We have players from PST, MST, CST, EST, BST, CEST, and MSK.

Our main days are 18:00 EST every Saturday. Occasionally, we may run operations at 18:00 EST on Sunday or Friday.
 
## Roles, not Ranks
We do not privilege players with medals or ranks just because they have been with a unit for a long time. Roles are given to those who ask for it. Our structure allows anyone choose any role, whether it be squad leader, sniper, UAV operator, etc. as we trust you can fulfill the responsibility. Players do not have to commit to a particular role and are open to switch any time.

## Stories that Mean Something
Every operation has a story, whether it be tied to our unit's canon or is it's own thing. The story makes the setting and operations change the story. Players fight for a reason, for the story, and every objective affects the story. We avoid generic "you're the good guys, they're the bad guys" stories.

And if you don't care about the story, you can avoid it.

## Active Community

We play games every night. If you are looking for a community of friends, we are always welcoming.

***
# Media
All media is linked and provided on the [S.E.S.O. Youtube Channel](https://www.youtube.com/channel/UC5iMX4ubNxfiFaG2fbAOKOg/featured).

## Recommended S.E.S.O. videos:

[Operation Green Diamond | 5th Engagement](https://www.youtube.com/watch?v=yiBY-arKDqI), full operation footage from an operation set in the Chernobyl Exclusion Zone.

[Operation Osiris Trailer](https://youtu.be/u7_2CUmIuQ8), a trailer for a campaign set in a post apocalyptic Chernarus.

[SESO in: "The Reconstruction of Mankind"](https://youtu.be/6i9VOpU5CWk), a collection of clips from the community showcasing us.

[Operation Perun | Final Engagement](https://www.youtube.com/watch?v=wnNviA-t7UU), a personal favorite. A 3 month campaign that ended with a bang.

[Operation Trebuchet | Side Campaign](https://www.youtube.com/watch?v=fLH6BiG3RD8), a collage from our Operation Trebuchet campaign set in the Halo universe.

[SESO Arma funny moments | Compilation of Silliness](https://www.youtube.com/watch?v=sqokKzQn9vc), another perfect example of our casual attitude.

***
# How Do I Join S.E.S.O?
First, join our discord: https://discord.gg/umGXdNgs8A

Second, if you are new to Arma, check out our New Operative Guide here: https://wiki.sesounit.org/guides/new_operative

***
"""
subreddit = reddit.subreddit('FindAUnit')
submission = subreddit.submit_image(
	'[NA][Recruiting][Casual][A3] S.E.S.O. | Variety with Common Sense Realism',
	'/home/arma3server/bot/Kakapo/result.jpg'
)
submission.reply(s)
