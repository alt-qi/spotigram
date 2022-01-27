from psycopg2 import OperationalError
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import utils
import os

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write(
'''
# Telegram bot token
bot_token = "INSERT YOUR BOT TOKEN HERE"

# Spotify Application Client ID
spotify_client_id = "INSERT YOUR SPOTIFY CLIENT ID HERE"

# Database creditionals 
database = "INSERT DATABASE NAME HERE"
user = "INSERT DATABASE USER NAME HERE",
password = "INSERT DATABASE USER PASSWORD HERE",
port = "INSERT DATABASE PORT HERE"
''')
        file.close()
        
    print("I have created a \".env\" file, fill required fields (token and database creditionals) in it, please.")
    exit()

try:
    utils.db.init()
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

# @dp.message_handler(commands=["auth"])
# async def auth(message: types.Message):
#     await message.answer(f"`{utils.spotify.generate_token()}`", parse_mode="MarkdownV2")

if __name__ == '__main__':
    executor.start_polling(dp)