import praw, time
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("reddit_tokens()")
reddit = praw.Reddit(user_agent= token.user_agent,
		  client_id= token.client_id,
		  client_secret= token.client_secret,
		  redirect_uri= token.redirect_uri,
		  username= token.username,
		  password= token.password)

print(reddit.user.me())



s = """[A round green and gray round shield with an 11-starred field and Kākāpō charge](https://imgur.com/GQGcVS8)

[SESO Operatives entrenched in a forest](https://imgur.com/a/MgVYSF6)
***


###Why choose S.E.S.O.?
* Casual milsim. This means no worries about military rank structure but still adhering to Veteran difficulty and common sense tactics.

* We have operations every Saturday evening.

* Low expectations. We require no experience, no test, no age limit, no commitment, and no sign-up. We will teach you everything you have to know in an hour.

* A dedicated server that constantly plays scenarios like Antistasi, TRGM2, Liberation, etc.

* Fleshed out campaigns in which players influence the outcomes of entire wars by completing their objectives in various ways

* An active lounge where we play various games every night (Paradox Grand Strategies, Garry's Mod, Rainbow Six Siege, Left 4 Dead 2, etc.).

###Current S.E.S.O. Campaign Details
S.E.S.O. is set an alternative history version of the 2014 Crimean conflict. The UN General Assembly Resolution 68/262 superceded the UN Security Council and sent peacekeeping forces to the afflicted region of Bystrica. Thinking it would be a simple operation, three PMCs were contracted for this conflict, one of which is S.E.S.O. The three PMCs work together to attempt to neutralize the Novorossiyan threat until it quickly runs out of control due to poor Ukrainian morale, human rights abuses, and xenophobia. It comes to S.E.S.O. operatives to to shape the outcome of this conflict any way they wish.

###Still not convinced?
Then hop on the [Discord](https://discord.gg/mVSYcdf) and see for yourself.
***

#**What is S.E.S.O.?**
S.E.S.O. is a private military group specialized in combined armed assaults, military sabotage, and HVT security. We receive contracts from all sorts of independent entities, supranational organizations, and armed forces.

We emerged as a group of friends with the aim of producing plain fun Zeus missions. That aim has still been true to the this day. We have weekly operations that could range from 3-5 hours. There is no commitment, no sign-up, and no requirements either. Simply download the mods, join the discord, join the teamspeak, and then join the server!

###We can best be contacted through our Discord below!
Discord: https://discord.gg/mVSYcdf"""

subreddit = reddit.subreddit('FindAUnit')
subreddit.submit(
	'S.E.S.O. [US][Recruiting][Casual][A3]', 
	selftext=s,)
