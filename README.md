# Discord League Notifications

> A Discord bot that watches your friends' League of Legends accounts and sends each of them a (usually
> mocking) direct message as soon as a game ends. Messages are AI-generated or picked from ones your server
> writes itself.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![Riot API](https://img.shields.io/badge/Riot_Games_API-D32936?logo=riotgames&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

## Features

- **Automatic game detection.** Every minute, the bot polls the Riot **Match-v5** API for each tracked player
  and detects games that just finished.
- **Win/loss aware.** It looks up the match result and sends a matching message by DM.
- **AI-generated trash talk.** Messages are generated with an OpenAI completion model using a few-shot prompt
  of example win and loss messages.
- **Custom messages.** Your server can add its own win/loss messages for each player. The more custom
  messages a player has, the more likely one is used instead of an AI one.
- **Templated messages.** Messages can reference `{player.name}` and any field of the Riot match object
  (`{game[...]}`).
- **Persistent storage** of player ↔ League account ↔ Discord user links, through
  [`dataset`](https://dataset.readthedocs.io/) (SQLite by default, any SQLAlchemy URL works).
- **Paginated embeds** for listing tracked players.

## Commands

All commands use the `!lb` prefix. Use `!lb help` to see them in Discord.

| Command | Description |
| --- | --- |
| `!lb add <name> <summoner_name> <discord_id>` | Start tracking a player and link their League account to a Discord user |
| `!lb del <name>` | Stop tracking a player |
| `!lb list` | Show tracked players (paginated) |
| `!lb clear_list` | Remove every tracked player |
| `!lb add_win_message <name> "<message>"` | Add a custom message a player can receive after a win |
| `!lb add_lose_message <name> "<message>"` | Add a custom message a player can receive after a loss |
| `!lb msg win\|lose` | Preview a generated message |

> Wrap names or messages that contain spaces in quotes, e.g. `!lb add "My Bro" "Bro Best Player" 1212145964539127`.
> To copy a Discord user ID, enable *Developer Mode* (Settings → Advanced), then right-click the user → *Copy User ID*.

## Getting started

### 1. Get the API keys

| Key | Where to get it |
| --- | --- |
| `DISCORD_API_KEY` | [Create a bot application and invite it to your server](https://discordpy.readthedocs.io/en/stable/discord.html) |
| `RIOT_API_KEY` | [Riot Developer Portal](https://developer.riotgames.com/docs/portal#_getting-started). Development keys expire every 24 h; register an app for a permanent one |
| `OPENAI_API_KEY` | [OpenAI platform](https://platform.openai.com/api-keys) |

### 2. Configure

```bash
git clone https://github.com/Reathe/Discord-League-Notifications
cd Discord-League-Notifications
cp .env.example .env
```

Then fill in `.env`:

```bash
DISCORD_API_KEY=your_discord_bot_token
RIOT_API_KEY=RGAPI-...
OPENAI_API_KEY=sk-...
DATABASE_URL='sqlite:///../league_bot.db'
```

### 3. Run

**With Docker**

```bash
docker build --tag discord-league-notif .
docker run -d --name dln-container discord-league-notif
```

**With Python 3.8**

```bash
pip install -r requirements.txt
python src/main.py
```

## Architecture

```
src/
├── main.py                 # Bot setup, commands, polling loop (every 60 s)
├── messages.py             # Message selection: AI-generated vs. custom, templating
├── player_account_link.py  # Player ↔ League PUUID ↔ Discord ID model
├── api/
│   ├── league_api.py       # Riot API: summoner lookup, match list, match details, win detection
│   └── openai_api.py       # OpenAI completion wrapper
└── database/
    ├── database.py         # Abstract dict-like repository interface
    └── dataset_db.py       # `dataset` (SQLAlchemy) implementation
```

Storage sits behind an abstract `MyDataBase` interface (`get`, `set`, `pop`, iteration, `in`), so the backend
can be replaced without touching the bot logic.

## Project status

Built in 2021 and pinned to the libraries of that time (`discord.py` 1.7, `openai` 0.11). Some APIs it uses
have since been retired upstream: the OpenAI `davinci` completion engine, and Riot's lookup of summoners by
name, which has been replaced by Riot IDs. Running it today would need those two calls updated.

## License

[GPL-3.0](LICENSE)
