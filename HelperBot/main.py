import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher import FSMContext
from handlers.setup import setup_handlers
from config import API_TOKEN
from utils.time_dispatcher import *

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = JSONStorage("data.json")
dp = Dispatcher(bot=bot, storage=storage,  loop=asyncio.get_event_loop())
time_dp = TimeDispatcher(bot)
setup_handlers(dp, time_dp)


if __name__ == "__main__":
    dp.loop.create_task(time_dp.start_updating())
    executor_thread = executor.start_polling(dp)
