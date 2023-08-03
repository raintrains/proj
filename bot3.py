from dotenv import dotenv_values
import sqlite3
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from db_dishes import create_db_dishes, get_price_dish, get_items
from db_clients import create_db_clients, update_db_clients, get_all
from asprise_api import asprise_process

from clear_data import refresh_bot

bot = Bot(token=dotenv_values(".env").get("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.DEBUG)

# start
dp.middleware.setup(LoggingMiddleware())




class MyStates(StatesGroup):
    WAITING_FOR_PHOTO = State()
    WAITING_FOR_NAME = State()
    WAITING_FOR_CHOICE = State()
    WAITING_CONTINUE_OR_NOT = State()
    CLEAR_DATA = State()


@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    await message.answer("Загрузите фото!")
    await MyStates.WAITING_FOR_PHOTO.set()
    create_db_clients()

    


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=MyStates.WAITING_FOR_PHOTO)
async def handler_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    await photo.download(r"photos/receipt.jpg")
    await message.answer("Фото успешно сохранено!")
    # asprise_process(r"photos/receipt.jpg")
    # create_db_dishes()

    await waiting_name(message, state)


async def waiting_name(message: types.Message, state: FSMContext):
    # await state.finish()
    await message.answer("Введите имя: ")
    await MyStates.WAITING_FOR_NAME.set()


# Функция для создания inline-клавиатуры с кнопками
def create_inline_keyboard(items):
    buttons = [
        types.InlineKeyboardButton(f"{item[0]}: {item[1]}грн", callback_data=str(item[0]))
        for item in items
    ]
    buttons.append(types.InlineKeyboardButton("Готово", callback_data="done"))
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)

    return keyboard


@dp.message_handler(state=MyStates.WAITING_FOR_NAME)
async def input_name(message: types.Message, state: FSMContext):
    entered_name = message.text
    await state.update_data(name=entered_name)
    items = get_items()
    keyboard = create_inline_keyboard(items)
    await message.reply("Выберите вариант из списка:", reply_markup=keyboard)
    await MyStates.WAITING_FOR_CHOICE.set()

    

@dp.callback_query_handler(lambda c: c.data not in ["done", "continue", "finalize"], state=MyStates.WAITING_FOR_CHOICE)
async def choice_dish(callback_query: types.CallbackQuery, state: FSMContext):
    
    selected_dish_id = callback_query.data
    dish_price = get_price_dish(selected_dish_id)

    await callback_query.answer(f"Добавлено {selected_dish_id}")

    if isinstance(dish_price, int):
        async with state.proxy() as order_amount:
            if "total_price" not in order_amount:
                order_amount["total_price"] = 0

            order_amount["total_price"] += dish_price

    
        
def buttons_finalize_continue():
    finalize_button = types.InlineKeyboardButton("Завершить", callback_data="finalize")
    continue_button = types.InlineKeyboardButton("Продолжить", callback_data="continue")
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(finalize_button, continue_button)

    return keyboard


@dp.callback_query_handler(lambda c: c.data == "done", state=MyStates.WAITING_FOR_CHOICE)
async def done_handler(callback_query: types.CallbackQuery, state: FSMContext):
    
    try:

        await callback_query.answer("Вы завершили выбор")   # Всплывающее окно
        data = await state.get_data()
        selected_name = data.get("name")
        total = data.get("total_price")
        update_db_clients(selected_name, total)

        await callback_query.message.answer(f"{selected_name}: {total} грн", reply_markup=buttons_finalize_continue())   # Выводиться как сообщение

        await MyStates.WAITING_CONTINUE_OR_NOT.set()
    
    except:

        await state.finish()

    

@dp.callback_query_handler(lambda c: c.data == "continue", state=MyStates.WAITING_CONTINUE_OR_NOT)
async def continue_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.reset_state()
    await waiting_name(callback_query.message, state)
    

@dp.callback_query_handler(lambda c: c.data == "finalize", state=MyStates.WAITING_CONTINUE_OR_NOT)
async def finalize_handler(callback_query: types.CallbackQuery, state: FSMContext):

    items = get_all()
    data = [(f"{name} - {total} грн") for name, total in items]
    
    text = ""

    for l in data:
        text += l + "\n"
        text += "\n"
    # result = tabulate(data, headers=["Имя", "Сумма"], tablefmt='fancy_grid')
    
    # max_lenght_name = len(max([tupl[0] for tupl in items], key=len))
    # max_total = len(str(max(tupl[1] for tupl in items)))
    
    button_close_session = types.InlineKeyboardButton("Начать с начала", callback_data="clear_data")
    keyboard = types.InlineKeyboardMarkup().add(button_close_session)

    await callback_query.answer()

    await callback_query.message.answer(text, reply_markup=keyboard)

    await MyStates.CLEAR_DATA.set()


@dp.callback_query_handler(lambda c: c.data == "clear_data", state=MyStates.CLEAR_DATA)
async def clear_data(callback_query: types.CallbackQuery, state: FSMContext):
    
    await state.reset_data()
    await state.reset_state()   # Переделать, вместо reset_data и reset_state написать await state.reset() и проверить на работоспособность!
    refresh_bot()
    await callback_query.answer()
    await on_start(callback_query.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)