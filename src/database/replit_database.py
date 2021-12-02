import replit
from database.database import MyDataBase
from player_account_link import PlayerAccountLink
from functools import singledispatchmethod


class MyReplitDB(MyDataBase):
    def remove(self, key):
        del replit.db[key]

    def set(self, key, link: PlayerAccountLink):
        replit.db.set(key, link.__dict__)

    def get(self, key) -> PlayerAccountLink:
        link = PlayerAccountLink('', '', '')
        link.__dict__ = replit.database.to_primitive(replit.db[key])
        link.custom_message = replit.database.to_primitive(link.custom_message)
        link.custom_message['true'] = replit.database.to_primitive(link.custom_message['true'])
        link.custom_message['false'] = replit.database.to_primitive(link.custom_message['false'])
        link.custom_message = {
            True: link.custom_message['true'],
            False: link.custom_message['false']
        }
        return link

    def __iter__(self):
        for key in replit.db.keys():
            yield self[key]

    def __len__(self):
        return len(replit.db)

    @singledispatchmethod
    def __contains__(self, item):
        raise NotImplementedError("Cannot negate a")

    @__contains__.register
    def __contains__name(self, name: str):
        return name in replit.db.keys()

    @__contains__.register
    def __contains__link(self, link: PlayerAccountLink):
        return any(link == temp_link for temp_link in self)
