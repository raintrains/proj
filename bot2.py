from dotenv import dotenv_values

TOKEN = dotenv_values(".env").get("TOKEN")

import sqlite3
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from db_dishes import create_db_dishes, get_price_dish, get_items
from db_clients import create_db_clients, update_db_clients
from asprise_api import asprise_process


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)



# start
dp.middleware.setup(LoggingMiddleware())



# Класс состояний FSM
class States(StatesGroup):
    INPUT_WORD = State()
    WAITING_FOR_CHOICE = State()



# Команда которая запрашивает фото и создает базу клиентов
@dp.message_handler(commands=["start"])
async def on_start(message: types.Message): 
    await message.answer("Загрузите фото!")




@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handler_photo(message: types.Message):

    photo = message.photo[-1]

    await photo.download(r"photos/receipt.jpg")
    # await ("Фото успешно сохранено!")

    # result_process = asprise_process(r"photos/receipt.jpg")

    # await message.answer(result_process)

    # create_db_dishes()

    await input_name(message)



# Функция для создания inline-клавиатуры с кнопками
def create_inline_keyboard(items):
    buttons = [
        types.InlineKeyboardButton(f"{item[0]}: {item[1]}грн", callback_data=str(item[0]))
        for item in items
    ]
    buttons.append(types.InlineKeyboardButton("Готово", callback_data="done"))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    return keyboard




@dp.message_handler(commands=["name"])
async def input_name(message: types.Message):
    await message.answer("Введите имя: ")

    await States.INPUT_WORD.set()




@dp.message_handler(state=States.INPUT_WORD)
async def proccess_word_input(message: types.Message, state: FSMContext):

    entered_name = message.text

    await state.update_data(name=entered_name)

    await on_start_db(message)



# start_db_dishes
async def on_start_db(message: types.Message, state: FSMContext):
    items = get_items()
    keyboard = create_inline_keyboard(items)
    await message.reply("Выберите вариант из списка:", reply_markup=keyboard)

    await States.WAITING_FOR_CHOICE.set()



@dp.callback_query_handler(lambda call: call.data == "done", state=States.WAITING_FOR_CHOICE)
async def done_handler(callback_query: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    selected_name = data.get("name")

    await callback_query.message.answer(f"Вы выбради {selected_name}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)











