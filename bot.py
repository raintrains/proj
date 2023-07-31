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


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)


# start
dp.middleware.setup(LoggingMiddleware())



# Функция для создания inline-клавиатуры с кнопками
def create_inline_keyboard(items):
    buttons = [
        types.InlineKeyboardButton(f"{item[0]}: {item[1]}грн", callback_data=str(item[0]))
        for item in items
    ]
    buttons.append(types.InlineKeyboardButton("Готово", callback_data="done"))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)
    return keyboard


# Обработчик inline-запросов
@dp.inline_handler(state=("*"))
async def inline_handler(query: types.InlineQuery, state: FSMContext):
    items = get_items()
    # Создание списка с inline кнопками
    results = []
    for item in items:
        text = f"{item[0]}: {item[1]}"
        result = types.InlineQueryResultArticle(
            id=str(item[0]),
            title=text,
            input_message_content=types.InputTextMessageContent(message_text=text),
            switch_pm_text = "Выберите вариант из списка",
            switch_pm_parameter = "start",
        )
        results.append(result)
    
    await query.answer(results=results, cache_time=1)



# Обработчик команды /db
@dp.message_handler(commands=["db"])
async def on_start_db(message: types.Message):
    items = get_items()
    keyboard = create_inline_keyboard(items)
    await message.reply("Выберите вариант из списка:", reply_markup=keyboard)

    await States.INPUT_SUM.set()

# Класс состояний FSM
class States(StatesGroup):
    INPUT_WORD = State()
    INPUT_SUM = State()


# # Обработчик текстового ввода от пользователя
@dp.message_handler(state=States.INPUT_WORD)
async def process_word_input(message: types.Message, state: FSMContext):

    # Получаем введеное слово и сохраняем его в состоянии пользователя
    entered_word = message.text
    await state.update_data(word=entered_word)

    # await state.finish()

    await message.answer(f'{message}')
    await on_start_db(message)



# Команда которая запрашивает фото и создает базу клиентов
@dp.message_handler(commands=["start"])
async def on_start(message: types.Message, state: FSMContext): 
    await message.answer("Загрузите фото!")

    create_db_clients()
    create_db_dishes()



# Обработчик команды /name
@dp.message_handler(commands=["name"])
async def input_name(message: types.Message):
    await message.answer("Введите имя: ")

    # Сохраняем состояние пользователя, чтобы ожидать ввод слова 
    await States.INPUT_WORD.set()



@dp.callback_query_handler(lambda query: True)
async def inline_callback_handler(callback_query: types.CallbackQuery):

    data = callback_query.data.strip()


    await callback_query.answer(f"Вы выбрали {data}")

    if data == "done":
        await callback_query.message.answer("DONE")


@dp.callback_query_handler(lambda query: True)
async def handle_inline_callback(callback_query: types.CallbackQuery):

    selected_dish_id = callback_query.data.strip()
    selected_dish = get_price_dish(selected_dish_id)
    if isinstance(selected_dish, int):

        await callback_query.answer(f"Price selected dish: {selected_dish}", show_alert=True)
        # await callback_query.answer(f"Текущая сумма {current_sum}")
    else:
        await callback_query.answer("Ошибка")



@dp.message_handler(state=States.INPUT_SUM, commands=["done"])
async def on_done(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_sum = data.get("current_sum", 0)
        name_client = data.get("word", "")
        update_db_clients(name_client, current_sum)

    await state.finish()
    await message.answer("Done!")


# end

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handler_photo(message: types.Message):

    photo = message.photo[-1]
    
    await photo.download(r"photos/receipt.jpg")

    await message.answer("Фото успешно сохранено!")





@dp.errors_handler()
async def errors_handler(update, exception):
    logging.error(f"Error handler updates {update}: {exception}")
    return True

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)











