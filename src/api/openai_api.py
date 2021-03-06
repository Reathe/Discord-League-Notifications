import os

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


async def request_completion(text, *args, **kwargs):
    """
    see https://beta.openai.com/docs/api-reference/ for arguments
    :param text: the text to autocomplete
    :return:
    """
    kwargs_ = {
        'engine': "davinci",
        'temperature': 0.9,
        'max_tokens': 100,
        'top_p': 0.6,
        'best_of': 3,
        'frequency_penalty': 0.05,
        'presence_penalty': 0,
        'stop': ["\n"],
        'logit_bias': {'60': -100}  # ']' character
    }
    for key in kwargs:
        kwargs_[key] = kwargs[key]
    kwargs = kwargs_
    return openai.Completion.create(
        *args,
        prompt=text,
        **kwargs
    )
