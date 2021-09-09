# Discord-League-Notifications
Send a message to your friends when their league game ends.

## Installation in your server
You have to host your bot yourself. You can also try the bot on [replit](https://replit.com) with this [branch](https://github.com/Reathe/Discord-League-Notifications/tree/replit) made for replit. 
### Discord bot creation
First you need to create a bot and add it to your server, just follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html).

### API Keys
You need the API keys for Discord and Riot games for this bot to work.

* For discord follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html).

* For Riot games, follow the instructions [here](https://developer.riotgames.com/docs/portal#_getting-started). For this one, you can either use the development API key given once you log in or register your bot to get an API key for it. If you chose to use the development API key, it will expire every 24h and you will have to copy it again from the developer portal

Once you have your API keys you need to create a file called `.env` inside this bot's directory. 

For example: `path/to/bot/Discord-League-Notifications/.env`

Inside the `.env` file you need to add your api key like this:
```bash
RIOT_API_KEY=RGAPI-6c498001-XXXX-XXXX-XXXX-3d7e0a483e04
DISCORD_API_KEY=ODE2MDXxXXX0MTI3MjIzMzQy.YD01-Q.xXxXXXXXxXlkKrHWiKBpI7Wwky7
```

## Executing the bot
You have two ways to do that.
#### With Docker
If you have [Docker](https://www.docker.com/) installed:
```bash
cd path/to/bot/Discord-League-Notifications
docker build --tag discord-league-notif .
docker run --name dln-container discord-league-notif
```
That's it ! Your bot should be running !
#### By yourself
With [python3](https://www.python.org/downloads/) installed:
```bash
cd path/to/bot/Discord-League-Notifications
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```
That's it ! Your bot should be running !

## Edit default received messages
For this, you need to edit the `messages.py` file.

The strings inside the `True` array are the ones sent on a win, and the `False` ones are sent on a lose. 

You can get the player's name via `link.name`. You can also use game information in the strings with the `game` parameter, it is an object  received from this api call [/lol/match/v5/matches/{matchId}](https://developer.riotgames.com/apis#match-v5/GET_getMatch). 
