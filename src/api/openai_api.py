import os

import openai

openai.api_key = os.environ['OPENAI_API_KEY']


def request_completion(text, *args, **kwargs):
    """
    see https://beta.openai.com/docs/api-reference/ for arguments
    :param text: the text to autocomplete
    :return:
    """
    if not kwargs:
        kwargs = {
            'engine': "davinci",
            'temperature': 1,
            'max_tokens': 100,
            'top_p': 1,
            'best_of': 10,
            'frequency_penalty': 0.1,
            'presence_penalty': 0,
            'stop': ["\n"],
            'logit_bias': {'60': -100}  # ']' character
        }

    return openai.Completion.create(
        *args,
        prompt=text,
        **kwargs
    )
