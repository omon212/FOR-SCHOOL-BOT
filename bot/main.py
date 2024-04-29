import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorag
from keyboards.default import keyboard_def
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import sqlite3
from states import CallbackStates


from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# ----------#

from aiogram.types import CallbackQuery

connect = sqlite3.connect('../db.sqlite3', check_same_thread=False)
cursor = connect.cursor()

API_TOKEN = '7035105679:AAHcWXjb97wm2DyH8le5juzsHNT2G9hGHu4'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

class Shogirdchala(StatesGroup):
    list_class = State()

@dp.message_handler(commands='start')
async def process_start_command(message: types.Message):
    await message.answer("Start", reply_markup=keyboard_def)

@dp.message_handler(text='Расписание классов')
async def class_schedule(message: types.Message, state: FSMContext):
    button_list = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 12)]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*button_list)
    await message.answer("Choose a class:", reply_markup=keyboard)
    await Shogirdchala.list_class.set()

@dp.callback_query_handler(state=Shogirdchala.list_class)
async def sinf_jadvali(call: types.CallbackQuery, state: FSMContext):
    class_number = int(call.data)
    cursor.execute("SELECT * FROM UserApp_studentstable WHERE class_number = ?", (class_number,))
    result = cursor.fetchall()
    print(result)
    await call.answer()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
