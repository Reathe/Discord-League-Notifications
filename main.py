import asyncio
import pickle
import sys
import traceback

from discord.ext import commands

from league_api import *
from messages import get_message

DISCORD_API_KEY = config['DISCORD_API_KEY']
links: Dict[str, 'PlayerAccountLink']
links = None
bot = commands.Bot(command_prefix='!lb ')


class PlayerAccountLink:
	def __init__(self, name, league_puuid, discord_id):
		self.name = name
		self.league_puuid = league_puuid
		self.discord_id = discord_id
		self.last_game = None

		self.custom_message: Dict[bool, List[str]]
		self.custom_message = {True: [], False: []}

	def __repr__(self):
		return \
			f'name = {self.name}\n' \
			f'league_puuid = {self.league_puuid}\n' \
			f'discord_id = {self.discord_id}\n' \
			f'last_game = {self.last_game}\n' \
			f'custom messages = {self.custom_message}\n'

	def __eq__(self, other):
		return (other.league_puuid == self.league_puuid and other.discord_id == self.discord_id) or other.name == self.name


def dump_links():
	global links
	with open('player_list.pickle', 'wb+') as db:
		pickle.dump(links, db)


def load_links():
	global links
	with open('player_list.pickle', 'rb+') as f:
		try:
			links = pickle.load(f)
		except EOFError:
			traceback.print_exc()
			links = {}
			dump_links()


def list_links() -> str:
	res = '```python\n[\n'
	for key in links.keys():
		link = links[key]
		res += link.__repr__() + ',\n'
	res += ']```'
	return res


@bot.event
async def on_ready():
	load_links()
	await init_last_played_games()
	while True:
		await asyncio.sleep(60)
		await loop()


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
	global links
	links = {}
	dump_links()
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
	global links
	try:
		links.pop(name)
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
	if len(links) > 50:
		await ctx.send('too many links, delete some')
		return

	try:
		new_link = PlayerAccountLink(player_name, await request_puuid_byname(summoner_name), discord_id)
		if any(link == new_link for link in links.values()):
			await ctx.send('Error: link or name already in list')
			return
		new_link.last_game = (await player_matchlist(new_link.league_puuid))[0]
		await bot.fetch_user(new_link.discord_id)
		links[new_link.name] = new_link
		dump_links()
		await ctx.send(f'added new link: {new_link}')
	except Exception:
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
	if message in links[name].custom_message[True]:
		await ctx.send(f'{name} can already receive this message when he wins.')
		return
	links[name].custom_message[True].append(message)
	dump_links()
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
	if message in links[name].custom_message[False]:
		await ctx.send(f'{name} can already receive this message when he loses.')
		return
	links[name].custom_message[False].append(message)
	dump_links()
	await ctx.send(f'{name} can now receive this message when he loses.')


async def init_last_played_games():
	for player in links.values():
		try:
			player.last_game = (await player_matchlist(player.league_puuid))[0]
		except Exception as e:
			print(e, file=sys.stderr)
			traceback.print_exc()
			print('riot donne pas les stats (' + player.name + ')')


async def loop():
	global links
	for player in links.values():
		try:
			# print(data)
			match_list = await player_matchlist(player.league_puuid, int(time.time())-60*5)
			if len(match_list) > 0:
				gameId = match_list[0]
				if gameId != player.last_game:
					player.last_game = gameId
					game = await get_game(gameId)

					try:
						user = await bot.fetch_user(player.discord_id)
						mess = get_message(is_win(game, player.league_puuid), player, game)
						await user.send(mess)
					except Exception as e:
						print(e, file=sys.stderr)
						traceback.print_exc()
						print("Impossible d'envoyer à " + str(player.name))

		except Exception as e:
			print(e, file=sys.stderr)
			traceback.print_exc()
			print('Riot game donne pas les stats (' + player.name + ')')
			continue
	dump_links()


if __name__ == '__main__':
	load_links()
	print(list_links())
	bot.run(DISCORD_API_KEY)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(fun())
