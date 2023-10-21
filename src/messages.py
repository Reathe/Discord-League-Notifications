import random
from math import exp

from .api.openai_api import request_completion
from .player_account_link import PlayerAccountLink

rand = random.Random()
lose_text = (
    "# Les messages drôles après avoir perdu une partie de League of Legends:\n"
    "messages = [\n"
    'f"haha alors ça lose bouffon?",\n'
    'f"ça arrive d\'être nul",\n'
    'f"Analyse du niveau de jeu de {player.name}... Claqué au sol",\n'
    'f"Si tu AFK, ton équipe aura peut-être une chance la prochaine fois!",\n'
    'f"rip les lp",\n'
    'f"Toujours les mates de merdes, jamais la faute de {player.name}",\n'
    "f\"En vrai t'as le niveau challenger, c'est juste unlucky\",\n"
    'f"La vie est injuste",\n'
)

win_text = (
    "# Les messages drôles après avoir gagné une partie de League of Legends:\n"
    "messages = [\n"
    'f"Bouffon de {player.name}, tu t\'es fait carry.",\n'
    'f"Vraiment que de la chance",\n'
    'f"En vrai t\'as bien joué... Pour un bronze",\n'
    'f"Heureusement qu\'ils jouent sans écran en face!",\n'
    'f"Estimation du niveau réel des adversaires: ... Claqué au sol",\n'
    'f"{player.name} a gagné ? Faudrait qu\'ils augmentent le niveau des bots",\n'
    "f\"Faut qu'on améliore le matchmaking... C'est pas normal que {player.name} gagne.\",\n"
)


async def get_message(win, player: PlayerAccountLink, game, *args, **kwargs):
    nb_custom_message = len(player.custom_message[win])
    prob_custom = (1 - (1 / exp(nb_custom_message / 8))) / 1.75

    if random.random() > prob_custom:
        response = await request_completion(
            win_text if win else lose_text, *args, **kwargs
        )
        msg = response.choices[0].text[2:-2]
    else:
        msg = rand.choice(player.custom_message[win])

    try:
        return msg.format(player=player, game=game)
    except KeyError:
        return msg.replace("{player.name}", player.name)
