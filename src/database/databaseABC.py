from abc import ABC, abstractmethod
from functools import singledispatchmethod

from database.player_account_link import PlayerAccountLink


class MyDataBase(ABC):
    def add(self, link: PlayerAccountLink):
        self.set(link.name, link)

    @abstractmethod
    def remove(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, link: PlayerAccountLink):
        pass

    @abstractmethod
    def get(self, key: str) -> PlayerAccountLink:
        pass

    def pop(self, key: str) -> PlayerAccountLink:
        link = self.get(key)
        self.remove(key)
        return link

    def __getitem__(self, key: str) -> PlayerAccountLink:
        return self.get(key)

    def __setitem__(self, key, link: PlayerAccountLink):
        self.set(key, link)

    def __delitem__(self, key: str):
        self.remove(key)

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @singledispatchmethod
    @abstractmethod
    def __contains__(self, item) -> bool:
        raise NotImplementedError("Cannot check if DB contains item")

    @__contains__.register
    @abstractmethod
    def _contains__name(self, name: str) -> bool:
        pass

    @__contains__.register
    @abstractmethod
    def _contains__link(self, link: PlayerAccountLink) -> bool:
        pass