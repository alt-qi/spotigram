"""
Модуль содержит в себе инструменты для работы со Spotify.
"""
from dataclasses import dataclass
import random
from urllib.parse import urlencode
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_URL = "https://accounts.spotify.com/authorize?"

@dataclass
class SpotifyTrack:
    """
    Этот дата-класс содержит в себе краткую информацию о
    треке Spotify.
    """
    title: str
    preview_audio_url: str
    performer: str
    full_version_url: str

class SpotifyClient(Spotify):
    """
    Этот класс содержит в себе функции для
    работы с данными пользователя Spotify.
    """
    def __init__(self, token: str, auth_manager: SpotifyOAuth) -> None:
        super().__init__(auth=token, auth_manager=auth_manager)

    def get_recently_played_tracks(self) -> list[SpotifyTrack]:
        """
        Возвращает недавно прослушанные пользователем треки.

        Returns:
            `list[SpotifyTrack]`: Список треков.
        """
        data = [track["track"] for track in self.current_user_recently_played(limit=5)["items"]]
        tracks = [
            SpotifyTrack(
                title=track["name"],
                preview_audio_url=track["preview_url"],
                performer=track["artists"][0]["name"],
                full_version_url=track['external_urls']['spotify']
            ) for track in data
        ]
        return tracks

class SpotifyApp(SpotifyOAuth):
    """
    Этот класс содержит в себе функции, необходимые
    для работы с интеграцией Spotify.
    """
    def __init__(self, client_id: str, client_secret: str,
                 redirect_uri: str, scopes: list[str]) -> None:
        super().__init__(client_id=client_id, client_secret=client_secret,
                         redirect_uri=redirect_uri, scope=" ".join(scopes))

    @staticmethod
    def generate_code(length=10, chars="1234567890abcdefg") -> str:
        """
        Сгенерировать код для привязки аккаунта Telegram к Spotify.

        Args:
            * length (`int`, optional): Длина, с которой нужно сгенерировать строку.
            * chars (`str`, optional): Строка, содержащяя символы, из которых будет состоять
            сгенерированная строка.

        Returns:
            `str`: Сгенерированная строка
        """
        return ''.join([random.choice(chars) for i in range(length)])

    def generate_url(self, code: str) -> str:
        """
        Сгенерировать ссылку для авторизации через Spotify OAuth 2.0.

        Args:
            * code (`str`): [description]

        Returns:
            `str`: Сгенерированная ссылка
        """
        return SPOTIFY_URL + urlencode({
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "response_type": "code",
                "scope": self.scope.replace(" ", "+"),
                "state": code
            }).replace("%2B", "+") # Символ "+" кодировать не нужно

    def get_spotify_client(self, token: str) -> SpotifyClient:
        """
        Авторизоваться в Spotify.

        Args:
            * token (`str`): токен для авторизации в Spotify.

        Returns:
            `SpotifyClient`
        """
        client = SpotifyClient(
            token=token,
            auth_manager=self
        )
        return client

# TODO: Реализовать обновление токена Spotify
