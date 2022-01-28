import random
from urllib.parse import urlencode, quote
from dotenv import load_dotenv
from copy import copy
from os import getenv

load_dotenv()

redirect_url = "http://localhost:8080/auth?"
spotify_url = "https://accounts.spotify.com/authorize?"
client_id = getenv("spotify_client_id")

params = {
    "client_id": client_id,
    "redirect_uri": redirect_url,
    "response_type": "code",
    "scope": "user-read-currently-playing",
}

def generate_code(length=10, chars="1234567890abcdefg"):
    return ''.join([random.choice(chars) for i in range(length)])

def generate_url(token):
    _params = copy(params)
    _params["code"] = token
    return (spotify_url + urlencode(_params)).replace("%25", "%")