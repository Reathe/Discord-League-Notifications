from functools import singledispatchmethod
from typing import Text

import dataset

from database import MyDataBase
from player_account_link import PlayerAccountLink


class DataSetDB(MyDataBase):
    def __init__(self):
        self.db: dataset.database.Database = dataset.connect()

    def remove(self, key: Text):
        with self.db as db:
            db['links'].delete(name=key)

    def set(self, key: Text, link: PlayerAccountLink):
        with self.db as tx:
            tx['links'].upsert(link.__dict__, ['name'])

    def get(self, key: Text) -> PlayerAccountLink:
        player = self.__get(key)
        return self.__construct_player_link(player)

    def __get(self, key: Text):
        return self.db['links'].find_one(name=key)

    @staticmethod
    def __construct_player_link(value) -> PlayerAccountLink:
        link = PlayerAccountLink('', '', '')
        link.__dict__ = value
        link.custom_message = {
            True: link.custom_message['true'],
            False: link.custom_message['false']
        }
        return link

    def __iter__(self):
        for player in self.db['links']:
            yield self.__construct_player_link(player)

    def __len__(self):
        return len(self.db['links'])

    @singledispatchmethod
    def __contains__(self, item):
        super().__contains__()

    @__contains__.register
    def _contains__name(self, name: str):
        return self.db['links'].find_one(name=name) is not None

    @__contains__.register
    def _contains__link(self, link: PlayerAccountLink):
        return (link.name in self) or \
               (self.db['links'].find_one(discord_id=link.discord_id, league_puuid=link.league_puuid) is not None)
