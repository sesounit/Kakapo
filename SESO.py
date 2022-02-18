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
**See our website for screenshots, briefings, wiki, merchandise, and more.**
https://www.sesounit.org/

***
# Schedule
We focus on on EST (Eastern United States) timezone. We have players from PST, MST, CST, EST, BST, CEST, and MSK.

Operation | Saturday | Sunday
:--|:--|:--
Operation Angola | 1800 EST |
Operation Osiris | TBA | TBA

***
# S.E.S.O.
SESO was established in 2018 with a focus on variety and story. We design 3-month long operations that are fun to play, easy to join, and contribute to the [SESO canon](https://wiki.sesounit.org/canon:list). We like to create The casual playstyle is tailored to allow one to join an operation as soon as possible. There is no required experience, minimum age, or test.

## Rankless Structure

We do not hold any ranks, in-game or out. Our structure allows anyone choose any role they wish, whether it be squad leader, sniper, UAV operator, etc. as long one fulfills their role. Players do not have to commit to a particular role and are open to switch roles every week.

## Canon

Operations set in the S.E.S.O. canon that span 90+ years. This means our operations can be set in any time period and setting, granting enormous variety. We have operated during the invasion of Czechoslovakia ([Sudeten Crisis, 1938](https://www.sesounit.org/timeline/operation-sudeten-crisis/)), the Vietnam War ([Operation Burning Buddhist, 1965](https://www.sesounit.org/timeline/operation-burning-buddhist/)), the Chernobyl Exclusion Zone ([Operation Green Diamond, 1988](https://www.sesounit.org/timeline/operation-green-diamond/)), and the Donbass War ([Crimean Crisis, 2014](https://www.sesounit.org/timeline/operation-crimean-crisis/)). We also operate in fictional settings that are based off historical events such as a Yugoslavian civil war set on Fapovo Islands ([Operation Openhouse, 1992](https://www.sesounit.org/timeline/operation-openhouse/)), and a southern African civil war on Isla Duala ([Isla Duala Civil War, 2000](https://www.sesounit.org/timeline/operation-isla-duala/)).

## Active Community

We play Arma 3 scenarios and other games every night. If you are looking for a community of friends, we are always welcoming.

***

#Media
All media is linked and provided on the [S.E.S.O. Youtube Channel](https://www.youtube.com/channel/UC5iMX4ubNxfiFaG2fbAOKOg/featured)

##Recommended S.E.S.O. videos:

[Operation Green Diamond | 5th Engagement](https://youtu.be/yiBY-arKDqI), full engagement footage from an operation set in the Chernobyl Exclusion Zone.

[Operation Burning Buddhist Trailer](https://www.youtube.com/watch?v=d8tj5IT-fi4), a trailer for our 5th operation set in the Vietnam War

[Operation Burning Buddhist | 2nd Engagement](https://www.youtube.com/watch?v=RlG4znKKK_E), full engagement footage of an engagement.

[Operation Trebuchet | Side Campaign](https://www.youtube.com/watch?v=fLH6BiG3RD8), a collage from our Operation Trebuchet campaign set in the Halo universe.

[Operation Perun | Final Engagement](https://youtu.be/wnNviA-t7UU), a personal favorite. A 3 month operation that ended with an explosive engagement.

[SESO Arma funny moments | Compilation of Silliness](https://youtu.be/sqokKzQn9vc). A perfect example of our casual attitude.

***

# How to Join S.E.S.O.
Follow the [New Operator Guide](https://wiki.sesounit.org/tutorials_guides:operator_guide) at our wiki.

If you have any questions, please join us in our Discord:
https://discord.gg/AVE9Gvq97C

***"""

subreddit = reddit.subreddit('FindAUnit')
submission = subreddit.submit(
	'[NA][Recruiting][Casual][A3] S.E.S.O. | Private Military Company', 
	selftext=s,)