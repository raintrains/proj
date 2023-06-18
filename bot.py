from dotenv import dotenv_values

TOKEN = dotenv_values(".env").get("TOKEN")


import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage



bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handler_photo(message: types.Message):

    photo = message.photo[-1]

    await photo.download(r"photos\\receipt.jpg")

    await message.answer("Photo has been saved!")

@dp.errors_handler()
async def errors_handler(update, exception):
    logging.error(f"Error handler updates {update}: {exception}")
    return True

if __name__ == '__main__':
    executor.start_polling(dp)