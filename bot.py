from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

if not ".env" in os.listdir():
    with open(".env", "w+") as file:
        file.write("bot_token = \"INSERT BOT TOKEN HERE\"")
        file.close()
        
    print("I have created a \".env\" file, fill \"bot_token\" field in it, please.")
    exit()

load_dotenv(".env")

try:
    bot = Bot(os.getenv("bot_token"))
except:
    print("Bot couldn't started! Please make sure, that token stored in \".env\" file is valid.")
    exit()

dp = Dispatcher(bot)

# @dp.message_handler()
# async def welcome(message: types.Message):
#     ...

executor.start_polling(dp)