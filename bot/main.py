import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.default import keyboard_def  # assuming you have a keyboard definition

# Set up logging
# logging.basicConfig(level=logging.INFO)

# Connect to SQLite database
connect = sqlite3.connect('/home/sharif/PycharmProjects/FOR SCHOOL BOT/db.sqlite3', check_same_thread=False)
cursor = connect.cursor()

# Bot token
API_TOKEN = '7035105679:AAHcWXjb97wm2DyH8le5juzsHNT2G9hGHu4'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# dp.middleware.setup(LoggingMiddleware())

# States definition
class Shogirdchala(StatesGroup):
    list_class = State()
    class_data = State()
    teacher_data = State()
    zvanok = State()


# Handlers
@dp.message_handler(commands='start')
async def process_start_command(message: types.Message):
    await message.answer("Start", reply_markup=keyboard_def)


@dp.message_handler(text="Расписание классов")
async def class_schedule(message: types.Message, state: FSMContext):
    await message.delete()
    button_list = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 12)]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*button_list, )
    await message.answer("Sinflardan birini tanlang:", reply_markup=keyboard)
    await Shogirdchala.list_class.set()


@dp.callback_query_handler(state=Shogirdchala.list_class)
async def sinf_jadvali(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    class_number = int(call.data)
    cursor.execute("SELECT * FROM UserApp_studentstable WHERE class_number = ?", (class_number,))
    result = cursor.fetchall()
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in result:
        button_text = f"{i[1]} {i[2]}"
        button_callback_data = f"{i[0]}"
        button = InlineKeyboardButton(text=button_text, callback_data=button_callback_data)
        keyboard.add(button)
    await call.message.answer(str(class_number), reply_markup=keyboard)
    await state.finish()
    await Shogirdchala.class_data.set()


@dp.callback_query_handler(state=Shogirdchala.class_data)
async def classss(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = int(call.data)
    cursor.execute("SELECT * FROM UserApp_studentstable WHERE id = ?", (data,))
    result = cursor.fetchall()
    print(result[0][3])
    photo = open(f'/home/sharif/PycharmProjects/FOR SCHOOL BOT/{result[0][3]}', 'rb')
    caption = f"Sinf raqami : {result[0][1]} {result[0][2]}"
    await call.message.answer_photo(photo=photo, caption=caption)
    await state.finish()


@dp.message_handler(text="Расписание учителей")
async def list_teacherss(message: types.Message):
    await message.delete()
    teachers_data = cursor.execute("SELECT * FROM UserApp_teachertablemodel ").fetchall()
    if teachers_data:
        keyboard = InlineKeyboardMarkup(row_width=4)
        for i in teachers_data:
            button = InlineKeyboardButton(text=str(i[1]), callback_data=str(i[1]))
            keyboard.add(button)
        await message.answer("Ustozlar royhati", reply_markup=keyboard)
        await Shogirdchala.teacher_data.set()
    else:
        await message.answer("Hali ustozlar royhati ma'lumotlari mavjud emas.")


@dp.callback_query_handler(state=Shogirdchala.teacher_data)
async def teacheddata(call: types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    data = str(call.data)
    result = cursor.execute("SELECT * FROM UserApp_teachertablemodel WHERE fio_teacher = ?", (data, )).fetchone()
    photo = open(f'/home/sharif/PycharmProjects/FOR SCHOOL BOT/{result[2]}', 'rb')
    await call.message.answer_photo(photo=photo,caption=f"""
FIo teacher: {result[1]}    
    """)
    await state.finish()



@dp.message_handler(text='Время Звонков')
async def chiqishvaqt(message: types.Message):
    await message.delete()
    data = cursor.execute("SELECT * FROM UserApp_calltimesmodel ").fetchall()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data:
        button = InlineKeyboardButton(text=str(i[1]), callback_data=str(i[0]))
        keyboard.add(button)
    await message.answer("Vremya zvanok:", reply_markup=keyboard)
    await Shogirdchala.zvanok.set()

@dp.callback_query_handler(state=Shogirdchala.zvanok)
async def zvanokjadval(call:types.CallbackQuery,state:FSMContext):
    await call.message.delete()
    data = int(call.data)
    i = cursor.execute("SELECT * FROM UserApp_calltimesmodel where id = ?",(data,)).fetchone()
    photo = open(f'/home/sharif/PycharmProjects/FOR SCHOOL BOT/{i[2]}', 'rb')
    await call.message.answer_photo(photo=photo, caption=f"""
Kun: {i[1]}     
    """)
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
