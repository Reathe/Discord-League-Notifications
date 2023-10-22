import requests
from dotenv import load_dotenv

load_dotenv()


def request_completion(text, *args, **kwargs):
    data = {
        "prompt": text,
        "temperature": 0.9,
        "max_tokens": 100,
        "top_p": 0.6,
        "frequency_penalty": 0.05,
        "presence_penalty": 0,
        "stop": ["\n"],
        "logit_bias": {"60": -100},
    }
    return requests.post(
        "http://localhost:8000/v1/completions",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json=data,
        timeout=40,
        *args,
        **kwargs,
    ).json()
