from aiogram.dispatcher.filters.state import State, StatesGroup


class CallbackStates(StatesGroup):
    chala = State()
    Students = State()
    Teacher = State()
    calltimes = State()
