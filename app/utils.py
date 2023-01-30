from datetime import datetime, timedelta, timezone
from typing import Tuple

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .keyboards import get_time_kb
from .states import UserTimezone


def iso_dt(dt: str) -> datetime:
    return datetime.fromisoformat(dt)


def hm_dt(dt: datetime, tz: timezone) -> str:
    return dt.astimezone(tz).strftime('%H:%M')


async def set_user_tz(shift: int, state: FSMContext) -> None:
    await state.set_state(UserTimezone.shift)
    await state.update_data(shift=shift)
    await state.set_state(None)


async def get_user_tz(state: FSMContext) -> timezone:
    msc_shift = 180
    await state.set_state(UserTimezone.shift)
    user_data = await state.get_data()
    await state.set_state(None)
    if 'shift' in user_data:
        return timezone(timedelta(minutes=user_data['shift']))
    return timezone(timedelta(minutes=msc_shift))


def process_programme(jr: dict, tz: int) -> Tuple[str, datetime, datetime]:
    sample = "<b>{}</b>\n<i>{} - {}</i>\n<b><i>{}</i></b>\n{}\n"
    prog = jr['Programme']
    desc = prog['pdesc'] if prog['pdesc'] else 'Содержание отсутствует'
    start, stop = iso_dt(prog['pstart']), iso_dt(prog['pstop'])
    values = (jr['disp_name'], hm_dt(start, tz),
              hm_dt(stop, tz), prog['title'], desc)
    return sample.format(*values), start, stop


async def answer_programme(prog: dict, ch_id: str, message: Message,
                           state: FSMContext):
    try:
        tz = await get_user_tz(state)
        text, start, stop = process_programme(prog, tz)
        await message.answer(
            text,
            reply_markup=get_time_kb(ch_id, start, stop),
            parse_mode='HTML'
        )
    except TypeError:
        await message.answer("К сожалению, программа отсутствует")
