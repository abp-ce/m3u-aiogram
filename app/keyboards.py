from datetime import datetime, timedelta, timezone
from typing import List

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .constants import TIMEZONES
from .factories import ListCF, ProgrammeCF, TimezoneCF


def get_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="По категориям")
    kb.button(text="По буквам")
    kb.button(text="Временная зона")
    kb.button(text="Локация", request_location=True)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_list_kb(items: List[dict], action: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for it in items:
        ad = {
            'categories': {'value': 'cat', 'text': 'cat'},
            'channels': {'value': 'ch_id', 'text': 'disp_name'}
        }
        text = it[ad[action]['text']] if it[ad[action]['text']] else 'Пусто'
        value = it[ad[action]['value']] if it[ad[action]['value']] else 'Пусто'
        kb.button(text=text, callback_data=ListCF(
            action=action,
            value=value
        ))
    kb.adjust(1)
    return kb.as_markup()


def get_time_kb(ch_id: str, start: datetime,
                stop: datetime) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data=ProgrammeCF(
        action='time',
        ch_id=ch_id,
        dt=(start - timedelta(minutes=1)).timestamp()
    ))
    kb.button(text='Сейчас', callback_data=ProgrammeCF(
        action='time',
        ch_id=ch_id,
        dt=datetime.now(tz=timezone.utc).timestamp()
    ))
    kb.button(text='Далее', callback_data=ProgrammeCF(
        action='time',
        ch_id=ch_id,
        dt=(stop + timedelta(minutes=1)).timestamp()
    ))
    return kb.as_markup()


def get_timezone_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for tzn in TIMEZONES:
        kb.button(text=tzn[0], callback_data=TimezoneCF(
            action='timezone',
            shift=tzn[1]
        ))
    kb.adjust(2)
    return kb.as_markup()
