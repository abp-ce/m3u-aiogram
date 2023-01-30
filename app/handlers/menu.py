from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..keyboards import get_menu_kb

router = Router()


@router.message(Command(commands=["menu"]))
async def cmd_start(message: Message):
    await message.answer("Привет!", reply_markup=get_menu_kb())


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message,  state: FSMContext):
    state.clear()
    await message.answer("Действие отменено")
