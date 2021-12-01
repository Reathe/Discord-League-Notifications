import asyncio
import os
import sys
import time
import traceback

from discord.ext import commands
from dotenv import load_dotenv

from api.league_api import get_game, is_win, player_matchlist, request_puuid_byname
from database.dataset_db import DataSetDB
from messages import get_message
from player_account_link import PlayerAccountLink

load_dotenv()
DISCORD_API_KEY = os.environ.get('DISCORD_API_KEY')

bot = commands.Bot(command_prefix='!lb ')

links_db = DataSetDB()


def list_links() -> str:
    link: PlayerAccountLink
    res = '```python\n[\n'
    for link in links_db:
        res += link.__repr__() + ',\n'
    res += ']```'
    return res


@bot.event
async def on_ready():
    await init_last_played_games()
    while True:
        try:
            await asyncio.sleep(60)
            await loop()
        except Exception as e:
            print(e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"No such command: {error}  (!lb help)")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing an argument: {error}")
        await ctx.send(f"```!lb {ctx.command} {ctx.command.signature}\n\n{ctx.command.help}```")
    else:
        raise Exception


@bot.command(name='list')
async def _list(ctx):
    """
    Shows the list of followed accounts

    Example:
        !lb list
    """
    res = list_links()
    await ctx.send(res)


@bot.command()
async def clear_list(ctx):
    """
    Clears the list of accounts to follow

    Example:
        !lb clear_list
    """
    global links_db
    link: PlayerAccountLink
    for link in links_db:
        del links_db[link.name]
    await ctx.send('Cleared links')


@bot.command(name='del')
async def _del(ctx, name):
    """
        Deletes a player from the list

        Notes:
            -You HAVE to add the quotes "" around the name if it contains spaces !

        Example:
            !lb del MyBro
            !lb del "My Best Bro"
    """
    global links_db
    try:
        links_db.pop(name)
        await ctx.send(f'Deleted {name}!')
    except KeyError:
        await ctx.send(f'{name} not in list')


@bot.command()
async def add(ctx, player_name, summoner_name, discord_id):
    """
    Adds a new player to follow, and links its league account to discord id

    Notes:
        -You HAVE to add the quotes "" around the name or summuner name if it contains spaces !
        -To get the user's Discord ID: enable 'developer mode' in discord settings under the 'advanced' tab,
        then right-click the user and select 'copy identifier'

    Example:
        !lb add MyBro "Bro Best Player" 121214596453912744
    """
    if len(links_db) > 50:
        await ctx.send('too many links, delete some')
        return

    try:
        new_link = PlayerAccountLink(player_name, await request_puuid_byname(summoner_name), discord_id)
        if any(link == new_link for link in links_db):
            await ctx.send('Error: link or name already in list')
            return
        new_link.last_game = (await player_matchlist(new_link.league_puuid))[0]
        await bot.fetch_user(new_link.discord_id)
        links_db.set(new_link.name, new_link)
        await ctx.send(f'added new link: {links_db[new_link.name]}')
    except Exception as e:
        """print(e, file=sys.stderr)
        traceback.print_exc()
        print(f'error add({player_name})')"""
        await ctx.send('Error adding the link... Check names and ids or try again later')

        m = type("", (), {})()
        m.name = 'None'
        raise commands.MissingRequiredArgument(m)


@bot.command()
async def add_win_message(ctx, name, message):
    """
    Adds a new message the user can receive when he wins!

    Notes:
        -You HAVE to add the quotes "" around the name or message if it contains spaces !

    Example:
        !lb add_win_message "My GIGA Bro" "Hahah told you you'd win!"
        !lb add_win_message MyBro "Lucky one..."
    """
    link = links_db.get(name)
    if message in link.custom_message[True]:
        await ctx.send(f'{name} can already receive this message when he wins.')
        return
    link.custom_message[True].append(message)
    links_db[link.name] = link
    await ctx.send(f'{name} can now receive this message when he wins.')


@bot.command()
async def add_lose_message(ctx, name, message):
    """
    Adds a new message the user can receive when he loses!

    Notes:
        -You HAVE to add the quotes "" around the name or message if it contains spaces !

    Example:
        !lb add_lose_message "My GIGA Bro" "Hahah told you you'd win... (everyone makes mistakes)"
        !lb add_lose_message MyBro "Unlucky one..."
    """
    link = links_db[name]
    if message in link.custom_message[False]:
        await ctx.send(
            f'{name} can already receive this message when he loses.')
        return
    link.custom_message[False].append(message)
    links_db[link.name] = link
    await ctx.send(f'{name} can now receive this message when he loses.')


async def init_last_played_games():
    for link in links_db:
        try:
            link.last_game = (await player_matchlist(link.league_puuid))[0]
        except Exception as e:
            print(e, file=sys.stderr)
            traceback.print_exc()
            print('riot donne pas les stats (' + link.name + ')')


@bot.command()
async def msg(ctx, win):
    """
    PLS don't abuse this command PILIZ VRAIMENT sinon jl'enleve
    Shows an example of a message you could get after a win/lose
    Example:
        !lb msg win
        !lb msg lose
    """
    res = await get_message('win' == win.lower(), PlayerAccountLink('NulBot', None, None), None, best_of=1)
    await ctx.send(res)


async def loop():
    global links_db
    link: PlayerAccountLink
    for link in links_db:
        try:
            # print(data)
            match_list = await player_matchlist(link.league_puuid, int(time.time()) - 60 * 5)
            if len(match_list) > 0:
                gameId = match_list[0]
                if gameId != link.last_game:
                    game = await get_game(gameId)
                    try:
                        user = await bot.fetch_user(link.discord_id)
                        mess = await get_message(is_win(game, link.league_puuid), link, game)
                        await user.send(mess)
                        link.last_game = gameId
                        links_db[link.name] = link
                    except Exception as e:
                        print(e, file=sys.stderr)
                        traceback.print_exc()
                        print("Impossible d'envoyer à " + str(link.name))

        except Exception as e:
            print(e, file=sys.stderr)
            traceback.print_exc()
            print('Riot game donne pas les stats (' + link.name + ')')
            continue


if __name__ == '__main__':
    print(list_links())
    bot.run(DISCORD_API_KEY)
