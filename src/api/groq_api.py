import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def request_completion(text, *args, **kwargs):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": 'Tu aimes dire des punchlines à tes amis lorsqu\'ils perdent une partie de League of Legends. \nTu incorpores parfois leur nom en écrivant "{player.name}".\nVoilà une liste d\'exemples de phrases que tu as déjà dis, mais tu ne dis jamais deux fois la même chose.\n\n\n"haha alors ça lose bouffon?",\n"ça arrive d\'être nul",\n"Analyse du niveau de jeu de {player.name}... Claqué au sol",\n"Si tu AFK, ton équipe aura peut-être une chance la prochaine fois!",\n"rip les lp",\n"Toujours les mates de merdes, jamais la faute de {player.name}",\n"En vrai t\'as le niveau challenger, c\'est juste unlucky",\n"La vie est injuste"',
            },
            {
                "role": "user",
                "content": "Je viens de perdre ma partie de League of legends",
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content
