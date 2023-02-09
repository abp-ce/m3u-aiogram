from datetime import datetime

import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import settings
from ..factories import ListCF, ProgrammeCF
from ..keyboards import get_list_kb
from ..states import ByLetters
from ..utils import answer_programme

router = Router()

BASE_URL = settings.backend_host + "/telebot/"


@router.message(F.text == 'По категориям')
async def categories(message: Message):
    r = httpx.get(BASE_URL + 'categories/')
    await message.answer("Выберите категорию",
                         reply_markup=get_list_kb(r.json(), 'categories'))


@router.callback_query(ListCF.filter(F.action == 'categories'))
async def callback_category(
        callback: CallbackQuery,
        callback_data: ListCF
):
    r = httpx.get(BASE_URL + f'category/{callback_data.value}')
    await callback.message.answer(
        'Выберите программу',
        reply_markup=get_list_kb(r.json(), 'channels')
    )


@router.callback_query(ListCF.filter(F.action == 'channels'))
async def callback_channel(
        callback: CallbackQuery,
        callback_data: ListCF,
        state: FSMContext
):
    r = httpx.get(BASE_URL + f'programme/{callback_data.value}')
    await answer_programme(r.json(), callback_data.value,
                           callback.message, state)


@router.callback_query(ProgrammeCF.filter(F.action == 'time'))
async def callback_time(
        callback: CallbackQuery,
        callback_data: ProgrammeCF,
        state: FSMContext
):
    time_str = datetime.fromtimestamp(float(callback_data.dt)).isoformat()
    r = httpx.get(
        BASE_URL + f'programme/{callback_data.ch_id}?dt={time_str}'
    )
    await answer_programme(r.json(), callback_data.ch_id,
                           callback.message, state)


@router.message(F.text == 'По буквам')
async def letters(message: Message, state: FSMContext):
    await message.answer("Введите часть названия канала")
    await state.set_state(ByLetters.letters)


@router.message(ByLetters.letters)
async def get_letters(message: Message, state: FSMContext):
    r = httpx.get(BASE_URL + f'letters/{message.text}')
    await message.answer(
        'Выберите программу',
        reply_markup=get_list_kb(r.json(), 'channels')
    )
    await state.clear()
