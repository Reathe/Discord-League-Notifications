import os
from typing import Any, Dict, List

import requests

RIOT_API_KEY = os.environ['RIOT_API_KEY']
header = {"X-Riot-Token": RIOT_API_KEY}


async def request(query: str, headers: Dict = None) -> Any:
    if headers is None:
        headers = header
    r = requests.get(query, headers=headers)
    if r is None:
        raise Exception('Riot API')
    data = r.json()
    return data


async def player_matchlist(league_puuid: str, timestamp=None, count=1) -> List:
    res = await request('https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + league_puuid + '/ids' +
                        f'?count={count}' +
                        (f'&startTime={timestamp}' if timestamp else ''))
    if not isinstance(res, list) or res is None or isinstance(res, dict):
        raise Exception(f'Riot API Error (puuid Error?) {res}')
    return res


async def request_puuid_byname(player_name: str) -> str:
    return (await request('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + player_name))['puuid']


async def get_game(gameId):
    game = await request('https://europe.api.riotgames.com/lol/match/v5/matches/' + str(gameId))
    return game


def is_win(game, puuid) -> bool:
    for player in game['info']['participants']:
        if player['puuid'] == puuid:
            return bool(player['win'])
