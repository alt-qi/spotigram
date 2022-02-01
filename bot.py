from psycopg2 import OperationalError
from aiogram import Bot, Dispatcher, executor, types, exceptions
from dotenv import load_dotenv
from utils import *
from os import getenv
import os
import hashlib

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write(
'''
# Telegram bot token
bot_token = "INSERT YOUR BOT TOKEN HERE"

# Spotify
spotify_client_id = "INSERT YOUR SPOTIFY APP CLIENT ID HERE"
spotify_client_secret = "INSERT YOUR SPOTIFY APP CLIENT SECRET HERE"
redirect_uri = "http://localhost:8080/auth?"

# Database creditionals 
database = "INSERT DATABASE NAME HERE"
user = "INSERT DATABASE USER NAME HERE",
password = "INSERT DATABASE USER PASSWORD HERE",
port = "INSERT DATABASE PORT HERE"
''')
        file.close()
        
    print("I have created a \".env\" file, please fill required fields in it.")
    exit()

load_dotenv(".env")

try:
    bot = Bot(os.getenv("bot_token"))
    db = database.Database(
        database=getenv("database"),
        user=getenv("user"),
        password=getenv("password"),
        port=getenv("port")
    )
except OperationalError:
    print("Failed to connect to database! Please make sure, that database creditionals stored in \".env\" are valid.")
    exit()
except exceptions.ValidationError:
    print("Bot failed to start! Please make sure, that token stored in \".env\" file is valid.")
    exit()

dp = Dispatcher(bot)

spotify_app = spotify.SpotifyApp(
    client_id=getenv("spotify_client_id"),
    client_secret=getenv("spotify_client_secret"),
    redirect_uri=getenv("redirect_uri"),
    scopes=["user-read-currently-playing", "user-read-recently-played"]
)

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer(f"Hello, `{message.from_user.full_name}`\!", parse_mode="MarkdownV2")

@dp.message_handler(commands=["auth"])
async def auth(message: types.Message):
    if not db.user_has_linked_spotify(message.from_user.id):
        auth_code = spotify_app.generate_code()
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text="Authorize Spotify",
            url=spotify_app.generate_url(auth_code)
        )
        keyboard.add(button)
        db.create_associate(message.from_user.id, auth_code)
        await message.answer("Click the button below to log into Spotify\.", reply_markup=keyboard, parse_mode="MarkdownV2")
    else:
        await message.answer(
            "*You already logged in\.*\n\n" \
            "If you want to reauthenticate, first use /logout", parse_mode="MarkdownV2")

@dp.message_handler(commands=["logout"])
async def logout(message: types.Message):
    if db.user_has_linked_spotify(message.from_user.id):
        db.remove_user_spotify_token(message.from_user.id)
        await message.answer(
            "*Auth information has been deleted*\.\n\n" \
            "If you want to start using the bot again, you will need to authenticate again with /auth", parse_mode="MarkdownV2")
    else:
        await message.answer(
            "*You are not authorized yet\.*\n\n" \
            "If you want to log in, use /auth", parse_mode="MarkdownV2")

@dp.inline_handler()
async def inline_echo(query: types.InlineQuery):
    text = query.query or "favorite_tracks"
    result_id = hashlib.md5(text.encode()).hexdigest()
    tracks = spotify_app.get_spotify_client(db.get_user_spotify_token(query.from_user.id)).get_recently_played_tracks()
    items = [
        types.InlineQueryResultAudio(
            id=spotify_app.generate_code(), 
            audio_url=track.preview_audio_url,
            title=track.title,
            performer=track.performer,   
            caption=f"__[Full Track Version]({track.full_version_url})__",
            parse_mode="MarkdownV2"
        ) for track in tracks
    ]
    await query.answer(results=items, cache_time=1)

if __name__ == '__main__':
    executor.start_polling(dp)