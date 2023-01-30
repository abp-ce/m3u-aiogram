from aiogram.filters.callback_data import CallbackData


class ListCF(CallbackData, prefix='list'):
    action: str
    value: str


class ProgrammeCF(CallbackData, prefix='prog'):
    action: str
    ch_id: str
    dt: float


class TimezoneCF(CallbackData, prefix='tz'):
    action: str
    shift: int
