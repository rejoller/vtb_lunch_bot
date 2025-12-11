import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from database.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker
from handlers import setup_routers

from zoneinfo import ZoneInfo
from logging_config import setup_logging
from logging_middleware import LoggingMiddleware

from users_middleware import UsersMiddleware
from chat_action_mw import ChatActionMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.triggers.cron import CronTrigger


from apscheduler.schedulers.asyncio import AsyncIOScheduler

#964635576
bot = Bot(os.getenv('BOT_TOKEN'))

      

async def main():
    from cron_jobs.jobs import get_menu
  #  bot = Bot(os.getenv('BOT_TOKEN'))
    storage = MemoryStorage()
    # storage = RedisStorage.from_url(os.getenv('REDIS_URL'), key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True))
    setup_logging()
    dp = Dispatcher(storage = storage)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))

    await create_db()
    import pytz

    moscow_tz = pytz.timezone("Europe/Moscow")

    async with session_maker() as session:
        scheduler = AsyncIOScheduler(timezone=moscow_tz)
        
        scheduler.add_job(
            get_menu,
            trigger=CronTrigger(
                day_of_week='mon-fri',  # только будние дни
                hour=17,
                minute=00,
                timezone=moscow_tz
            ),
            kwargs={"session": session}
        )

    scheduler.start()
    # await drop_db()
    router = setup_routers()
    dp.include_router(router)
    dp.update.middleware(ChatActionMiddleware())
    router.message.middleware(ChatActionMiddleware())
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(UsersMiddleware())
    print('Бот запущен и готов к приему сообщений')
    logging.info('--------------------Бот запущен и готов к приему сообщений------------------------------')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True)
    

if __name__ == "__main__":
    asyncio.run(main())
