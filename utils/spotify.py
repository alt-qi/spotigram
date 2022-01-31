import random
from aiogram.types import InlineQueryResultAudio, InputTextMessageContent
from . import db
from urllib.parse import urlencode, quote
from dotenv import load_dotenv
from copy import copy
from os import getenv
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

redirect_uri = getenv("redirect_url")
spotify_url = "https://accounts.spotify.com/authorize?"
client_id = getenv("spotify_client_id")
client_secret = getenv("spotify_client_secret")

params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": "user-read-currently-playing+user-read-recently-played",
}

def generate_code(length=10, chars="1234567890abcdefg"):
    return ''.join([random.choice(chars) for i in range(length)])

def generate_url(token):
    _params = copy(params)
    _params["state"] = token
    return (spotify_url + urlencode(_params)).replace("%25", "%").replace("%2B", "+")

def get_spotify_client(user_id):
    spotify = Spotify(
        auth=db.get_spotify_token(user_id),
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            scope="user-read-currently-playing user-read-recently-played",
            redirect_uri=redirect_uri
        )
    )
    return spotify

def get_recently_played_tracks(user_id):
    spotify = get_spotify_client(user_id)
    tracks = []
    tracks += [
        InlineQueryResultAudio(
            id=generate_code(),
            audio_url=track["track"]["preview_url"],
            title=track["track"]["name"],
            performer=track["track"]["artists"][0]["name"],   
            caption=f"__[Full Track Version]({track['track']['external_urls']['spotify']})__",
            parse_mode="MarkdownV2"
        )    
    for track in spotify.current_user_recently_played(limit=5)["items"]]
    return tracks