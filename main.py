import logging
import ssl

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types.input_file import FSInputFile
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp.web import Application, run_app

from app.config import settings
from app.handlers import locations, menu, programmes


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(
        f"{base_url}/webhook",
        certificate=FSInputFile(settings.pem_file)
    )
    commands = [
        types.BotCommand(command="menu", description="Выберите опцию"),
        types.BotCommand(command="cancel", description="Отменить действие")
    ]
    await bot.set_my_commands(commands)


def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=RedisStorage.from_url(url=settings.redis_host))
    dp.include_router(menu.router)
    dp.include_router(programmes.router)
    dp.include_router(locations.router)
    dp["base_url"] = settings.app_base_url
    dp.startup.register(on_startup)

    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(settings.pem_file, settings.key_file)

    run_app(app, host="0.0.0.0", ssl_context=ssl_context)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
