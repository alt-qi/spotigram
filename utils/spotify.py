import random
from urllib.parse import urlencode, quote
from copy import copy

redirect_url = "http://localhost:8080/auth?"
spotify_url = "https://accounts.spotify.com/authorize?"
client_id = "09f234ad396c4a74aa08b688006258e5"

params = {
    "client_id": client_id,
    "redirect_uri": redirect_url,
    "response_type": "code",
    "scope": "user-read-currently-playing",
}

def generate_token(length=10, chars="1234567890abcdefg"):
    return ''.join([random.choice(chars) for i in range(length)])

def generate_url(token):
    _params = copy(params)
    _params["code"] = generate_token()
    return (spotify_url + urlencode(_params)).replace("%25", "%")

print(generate_url(generate_token()))