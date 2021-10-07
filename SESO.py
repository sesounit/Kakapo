import praw, time, os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(user_agent= os.getenv("user_agent"),
		  client_id= os.getenv("client_id"),
		  client_secret= os.getenv("client_secret"),
		  redirect_uri= os.getenv("redirect_uri"),
		  username= os.getenv("username"),
		  password= os.getenv("password"))

print(reddit.user.me())



s = """#Media
All media is linked and provided on the [S.E.S.O. Youtube Channel](https://www.youtube.com/channel/UC5iMX4ubNxfiFaG2fbAOKOg/featured)

The following is a selection of recommended S.E.S.O. videos:

[Operation Green Diamond | 5th Engagement](https://youtu.be/yiBY-arKDqI), full engagement footage from an operation set in the Chernobyl Exclusion Zone.

[Operation Burning Buddhist Trailer](https://www.youtube.com/watch?v=d8tj5IT-fi4), a trailer for our 5th operation set in the Vietnam War

[Operation Burning Buddhist | 2nd Engagement](https://www.youtube.com/watch?v=RlG4znKKK_E), full engagement footage of an engagement.

[Operation Trebuchet | Side Campaign](https://www.youtube.com/watch?v=fLH6BiG3RD8), a collage from our Operation Trebuchet campaign set in the Halo universe.

[Operation Perun | Final Engagement](https://youtu.be/wnNviA-t7UU), a unit-favorite. A 3 month operation that ended with an explosive engagement.

[SESO Arma funny moments | Compilation of Silliness](https://youtu.be/sqokKzQn9vc). A perfect example of our casual attitude.

***
# Schedule
We operate in the EST timezone. However, we are open to all timezones, especially European and Pacific.

Operation | Saturday | Sunday
:--|:--|:--
S.E.S.O. Operation | 1800 EST | 1800 EST

***
# What we offer
## Casual MilSim Atmosphere

We focus on having fun first, being tactical later. This means many of our addons and structure are configured for maximum enjoyment with the the least drag.

## Low expectations

No experience, no test, no minimum age, no microphone needed, no single-clanning requirement. Just have Arma 3 and a desire for cooperation.

## Rankless structure

We do not hold any ranks in the unit, in-game or outside. Yet, we still hold a structure. Anyone is permissible to choose any role they wish, whether it be squad leader, sniper, pilot, etc. as long as most of the group agrees with the role selection. Usually, the group is fine with anyone's selection and the structure works harmoniously.

## S.E.S.O. Storyline Operations

Operations set in the S.E.S.O. canon are part of a storyline that spans several campaigns. This means our operations can be set in any time period and setting. We have operated during the invasion of Czechoslovakia (Sudeten Crisis, 1938), the Vietnam War (Operation Burning Buddhist, 1965), the Chernobyl Exclusion Zone (Operation Green Diamond, 1988), and the Donbass War (Operation Black Bear, 2014). We also operate in fictional settings that are based off historical events such as a Yugoslavian civil war set on Fapovo Islands (Operation Openhouse, 1992), and a Southern African civil war on Isla Duala (Isla Duala Civil War, 2000).

## 24/7 Scenarios Server

Our dedicated server machine runs community-made scenarios on rotation, always available to play any time. This is perfect for individuals who cannot make it to the operations but wish to spend time with S.E.S.O. It is also good for any people who just want more Arma 3 in their lives. The current scenarios we play are Antistasi (with RHS mods), Manhunt, and Dynamic Recon Ops. Feel free to suggest more workshop missions.

## Side Engagements

S.E.S.O. makes it easy for one to become a host of engagements/operations. Upon request and feedback from experienced Operation Hosts, one can quickly feature their custom-made missions to the unit. There is no strict test or experience necessary. With enough engagements under one's sleeve, one can even contribute to the S.E.S.O. storyline.

## Active Lounge

Every night, we gather in voice channels to play games. We are welcome for anyone to join in our multiplayer game sessions, developing mods, or just to chat.

***
# Background
In 2018, we grew dissatisfied with the strict bureacracy associated with Arma MilSim units. It was difficult to get into an engaging operation fast and easily. Thus, S.E.S.O. was created. We are a tightly knit community bent on providing engaging experiences where friends can cooperate without the overhead of ranks and tests. Since then, we have garnered 15+ active players per operation and we hope to garner more. We will keep posting for recruitment until our soft-cap of 32 active players. We welcome you to join us for one operation or many.

***

# How to Join S.E.S.O.

1. Join the discord at  https://discord.gg/AVE9Gvq97C
2. Download the mods you want in #mod-list
3. Join the Teamspeak Server using #teamspeak-info
4. Join the game server using the same connection details from #teamspeak-info

***"""

subreddit = reddit.subreddit('FindAUnit')
subreddit.submit(
	'S.E.S.O. PMC[US][Recruiting][Casual][A3]', 
	selftext=s,)
