from asyncio import exceptions
from psycopg2 import OperationalError
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from utils import *
import os

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write(
'''
# Telegram bot token
bot_token = "INSERT YOUR BOT TOKEN HERE"

# Spotify
spotify_client_id = "INSERT YOUR SPOTIFY CLIENT ID HERE"
redirect_url = "http://localhost:8080/auth?"

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
    db.init()
    bot = Bot(os.getenv("bot_token"))
except OperationalError:
    print("Failed to connect to database! Please make sure, that database creditionals stored in \".env\" are valid.")
    exit()
except exceptions.ValidationError:
    print("Bot failed to start! Please make sure, that token stored in \".env\" file is valid.")
    exit()

dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer(f"Hello, `{message.from_user.full_name}`\!", parse_mode="MarkdownV2")

@dp.message_handler(commands=["auth"])
async def auth(message: types.Message):
    if not db.user_token_exists(message.from_user.id):
        auth_code = spotify.generate_code()
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            text="Authorize Spotify",
            url=spotify.generate_url(auth_code)
        )
        keyboard.add(button)
        db.save_auth_code(message.from_user.id, auth_code)
        await message.answer("Click the button below to log into Spotify\.", reply_markup=keyboard, parse_mode="MarkdownV2")
    else:
        await message.answer(
            "*You already logged in\.*\n\n" \
            "If you want to reauthenticate, first use /logout", parse_mode="MarkdownV2")

@dp.message_handler(commands=["logout"])
async def logout(message: types.Message):
    if db.user_token_exists(message.from_user.id):
        db.remove_spotify_token(message.from_user.id)
        await message.answer(
            "*Auth information has been deleted*\.\n\n" \
            "If you want to start using the bot again, you will need to authenticate again with /auth", parse_mode="MarkdownV2")
    else:
        await message.answer(
            "*You are not authorized yet\.*\n\n" \
            "If you want to log in, use /auth", parse_mode="MarkdownV2")

# @dp.inline_handler()
# async def inline_echo(inline_query: types.InlineQuery):
#     ...

if __name__ == '__main__':
    executor.start_polling(dp)