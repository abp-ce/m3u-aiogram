from aiogram.fsm.state import State, StatesGroup


class UserTimezone(StatesGroup):
    shift = State()


class ByLetters(StatesGroup):
    letters = State()
