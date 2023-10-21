class PlayerAccountLink:
    def __init__(self, name, league_puuid, discord_id):
        self.name = name
        self.league_puuid = league_puuid
        self.discord_id = discord_id
        self.last_game = None

        self.custom_message: dict[bool, list[str]]
        self.custom_message = {True: [], False: []}

    def __repr__(self):
        return (
            f"name = {self.name}\n"
            f"league_puuid = {self.league_puuid}\n"
            f"discord_id = {self.discord_id}\n"
            f"last_game = {self.last_game}\n"
            f"custom messages = {self.custom_message}\n"
        )

    def __eq__(self, other):
        return (
            other.league_puuid == self.league_puuid
            and other.discord_id == self.discord_id
        ) or other.name == self.name
