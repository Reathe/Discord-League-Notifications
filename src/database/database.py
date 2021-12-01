from abc import ABC, abstractmethod
from typing import Text

from player_account_link import PlayerAccountLink


class MyDataBase(ABC):
    def add(self, link: PlayerAccountLink):
        self.set(link.name, link)

    @abstractmethod
    def remove(self, key: Text):
        pass

    @abstractmethod
    def set(self, key: Text, link: PlayerAccountLink):
        pass

    @abstractmethod
    def get(self, key: Text) -> PlayerAccountLink:
        pass

    def pop(self, key: Text) -> PlayerAccountLink:
        link = self.get(key)
        self.remove(key)
        return link

    def __getitem__(self, key: Text) -> PlayerAccountLink:
        return self.get(key)

    def __setitem__(self, key, link: PlayerAccountLink):
        self.set(key, link)

    def __delitem__(self, key: Text):
        self.remove(key)

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass
