import random

rand = random.Random()


def get_message(win, link, game):
	message = {
		False:
			[
				'haha alors ça lose bouffon?',
				'ça arrive d\'être nul',
				f'Analyse du niveau de jeu de {link.name}... Claqué au sol',
				f'Si tu AFK, ton équipe aura peut-être une chance la prochaine fois!'
			] + link.custom_message[False],
		True:
			[
				f'Bouffon de {link.name}, tu t\'es fait carry.',
				f'Vraiment que de la chance',
				f'En vrai t\'as bien joué... Pour un iron',
				f'Heureusement qu\'ils jouent sans écran en face!'
			] + link.custom_message[True]
	}
	return rand.choice(message[win])
