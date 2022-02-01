"""
Этот модуль содержит класс, содержащий инструменты для взаимодействия с базой данных.
"""
import psycopg2
from psycopg2.errors import DuplicateTable

class Database:
    """
    Этот класс реализует все необходимые для работы бота функции,
    которые связаны с базой данных.
    """
    def __init__(self, database: str, user: str, password: str, port: str) -> None:
        self.con = psycopg2.connect(database=database, user=user, password=password, port=port)
        self.cur = self.con.cursor()
        self.create_tables()
        self.reset_associates()

    def create_tables(self) -> None:
        """
        Создаёт в базе данных необходимые таблицы, если они отсутствуют.
        """
        try:
            self.cur.execute("CREATE TABLE spotify_tokens (user_id INTEGER, token TEXT)")
        except DuplicateTable:
            pass
        self.con.commit()
        try:
            self.cur.execute("CREATE TABLE associates (user_id INTEGER, code TEXT)")
        except DuplicateTable:
            pass
        self.con.commit()

    def reset_associates(self) -> None:
        """
        Стирает все добавленные в базу данных ассоциации аккаунтов Telegram
        с кодами для авторизации.

        P.S.: Коды нужны, чтобы сервер (https://github.com/alt-qi/spotigram-server)
        знал, к какому пользователю присваивать полученный после OAuth-авторизации
        токен Spotify.
        """
        self.cur.execute("DELETE FROM associates")
        self.con.commit()

    def associate_exists(self, user_id: str) -> bool:
        """
        Проверяет, существует ли код авторизации для указанного пользователя.

        Args:
            * user_id (`str`): id пользователя в Telegram.

        Returns:
            `bool`
        """
        self.cur.execute("SELECT EXISTS (SELECT * FROM associates WHERE user_id = %s)", (user_id,))
        return self.cur.fetchone()[0]

    def create_associate(self, user_id: str, code: str) -> None:
        """
        Сохраняет код для авторизации.

        Args:
            * user_id (`str`): id пользователя Telegram, с которым будет связан указанный код.
            * code (`str`): код для авторизации.
        """
        if not self.associate_exists(user_id):
            self.cur.execute("INSERT INTO associates VALUES (%s, %s)", (user_id, code))
        else:
            self.cur.execute("UPDATE associates SET code = %s WHERE user_id = %s", (code, user_id))
        self.con.commit()

    def user_has_linked_spotify(self, user_id: str) -> bool:
        """
        Проверяет, привязал ли пользователь свой аккаунт Spotify.

        Args:
            * user_id (`str`): id пользователя Telegram.

        Returns:
            `bool`
        """
        self.cur.execute("SELECT EXISTS (SELECT * FROM spotify_tokens WHERE user_id = %s)",
                         (user_id,))
        return self.cur.fetchone()[0]

    def get_user_spotify_token(self, user_id: str) -> str:
        """
        Возвращает токен для авторизации в аккаунт Spotify
        указанного пользователя.

        Args:
            * user_id (`str`): id пользователя Telegram

        Returns:
            `str`: токен Spotify
        """
        self.cur.execute("SELECT token FROM spotify_tokens WHERE user_id = %s", (user_id,))
        return self.cur.fetchone()[0]

    def remove_user_spotify_token(self, user_id: int) -> None:
        """
        Удаляет из базы данных токен аккаунта Spotify
        указанного пользователя.

        Args:
            * user_id (`int`): id пользователя Telegram
        """
        self.cur.execute("DELETE FROM spotify_tokens WHERE user_id = %s", (user_id,))
        self.con.commit()
