from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write(
'''
# Telegram bot token
bot_token = "INSERT YOUR BOT TOKEN HERE"

# Database creditionals 
database = "INSERT DATABASE NAME HERE"
user = "INSERT DATABASE USER NAME HERE",
password = "INSERT DATABASE USER PASSWORD HERE",
port = "INSERT DATABASE PORT HERE"
''')
        file.close()
        
    print("I have created a \".env\" file, fill required fields (token and database creditionals) in it, please.")
    exit()

import utils

load_dotenv(".env")

try:
    bot = Bot(os.getenv("bot_token"))
except:
    print("Bot couldn't started! Please make sure, that token stored in \".env\" file is valid.")
    exit()

dp = Dispatcher(bot)

@dp.message_handler()
async def welcome(message: types.Message):
    await message.answer(f"Hello, `{message.from_user.full_name}`\!", parse_mode="MarkdownV2")

# @dp.message_handler(commands=["auth"])
# async def auth(message: types.Message):
#     ...

if __name__ == '__main__':
    executor.start_polling(dp)