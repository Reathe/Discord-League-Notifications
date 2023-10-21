import sys
from os import path

from database.player_account_link import PlayerAccountLink

from database.dataset_db import DataSetDB

sys.path.append(path.join(path.dirname(__file__), ".."))

if __name__ == "__main__":
    db = DataSetDB()
    raf = PlayerAccountLink("raf", "discord", "league")
    db.add(raf)
    assert raf.name in db
    assert raf in db
    raf_copy = PlayerAccountLink("rafa", "discord", "league")
    assert raf_copy.name not in db
    assert raf_copy in db
    del db["raf"]
    assert raf not in db
