import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import   State, StatesGroup
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.dispatcher import FSMContext
import weather
from config import API_TOKEN
from btime.time_dispatcher import *

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
storage = JSONStorage("data.json")
dp = Dispatcher(bot=bot, storage=storage,  loop = asyncio.get_event_loop())
time_dp = timeDispatcher(bot)

class Form(StatesGroup):
    day_part = State()
    drug_name = State()

@dp.message_handler(commands=['weather'])
async def handleWeather(msg: types.Message):
    temperature, feels_like = await weather.get_wheather()
    await msg.answer(f"Сейчас температура: {round(temperature, 1)}\n Чувствуется как {round(feels_like, 1)}")    
    
@dp.message_handler(commands=['set_drug_helper'])
async def start_drug_helper(msg: types.Message):
    await Form.day_part.set()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Утро")
    markup.add("День")
    markup.add("Вечер")
    
    await msg.reply("Введите, когда принимать таблетки(утро,день,вечер).", reply_markup=markup)

@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(msg: types.Message, state = FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    logging.info("Canceling state {current_state}")
    
    await state.finish()
    await msg.reply("Cancelled", reply_markup=types.ReplyKeyboardRemove()   )

@dp.message_handler(lambda message: message.text not in ["Утро", "День", "Вечер"], state=Form.day_part)
async def procedd_day_part_invalid(msg: types.Message, state: FSMContext):
    return await msg.reply("Используйте кнопочки.")

@dp.message_handler(state=Form.day_part)
async def process_day_part(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["day_part"] = msg.text
           
        markup = types.ReplyKeyboardRemove()
           
        await msg.reply("Введите название лекарства", reply_markup=markup)
        await Form.next()
    state.storage.write(Path("data.json"))
 
@dp.message_handler(state=Form.drug_name)
async def process_drug_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["drug_name"] = msg.text
        time_dp.add_user_drug(msg.from_user, data["drug_name"], data["day_part"])
    await state.finish()
    await msg.reply("Спасибо!")
    state.storage.write(Path("data.json"))
      
@dp.message_handler()
async def not_handled_message_handler(msg: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    markup.add("/weather")
    markup.add("/set_drug_helper")
    
    await msg.answer("Вы можете:\n Узнать погодку: /weather\n" +
                      "Настроить напоминалку: /set_drug_helper", reply_markup=markup)
      


if __name__ == "__main__":
    dp.loop.create_task(time_dp.start_updating())
    executor_thread = executor.start_polling(dp)
          