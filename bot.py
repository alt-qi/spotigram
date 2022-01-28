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

try:
    db.init()
except OperationalError:
    print("Failed to connect to database! Please make sure, that database creditionals stored in \".env\" are valid.")

load_dotenv(".env")

try:
    bot = Bot(os.getenv("bot_token"))
except:
    print("Bot failed to start! Please make sure, that token stored in \".env\" file is valid.")
    exit()

dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    await message.answer(f"Hello, `{message.from_user.full_name}`\!", parse_mode="MarkdownV2")

@dp.message_handler(commands=["generateurl"])
async def generate_url(message: types.Message):
    auth_code = spotify.generate_code()
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Auth URL",
        url=spotify.generate_url(auth_code)
    )
    keyboard.add(button)
    db.save_auth_code(message.from_user.id, auth_code)
    await message.answer("Your link is ready!", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)