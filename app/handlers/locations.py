import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import settings
from ..constants import GEONAMES_URL
from ..factories import TimezoneCF
from ..keyboards import get_timezone_kb
from ..utils import set_user_tz

router = Router()


@router.message(F.text == 'Временная зона')
async def timesones(message: Message):
    await message.answer("Выберите временную зону",
                         reply_markup=get_timezone_kb())


@router.callback_query(TimezoneCF.filter(F.action == 'timezone'))
async def callback_time(
        callback: CallbackQuery,
        callback_data: TimezoneCF,
        state: FSMContext
):
    await set_user_tz(callback_data.shift, state)
    await callback.message.answer(
        f"Ваша временная зона: UTC + {callback_data.shift} мин."
    )


@router.message(F.location)
async def location(message: Message, state: FSMContext):
    minutes = 60
    loc = message.location
    values = (loc.latitude, loc.longitude, settings.geo_user)
    jr = httpx.get(GEONAMES_URL.format(*values)).json()
    if 'rawOffset' in jr:
        shift = int(jr['rawOffset'] * minutes)
        await set_user_tz(shift, state)
        await message.answer(
            f"Ваша временная зона: UTC + {shift} мин."
        )
