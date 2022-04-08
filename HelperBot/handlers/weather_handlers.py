from aiogram import types
import utils.weather as weather


async def handleWeather(msg: types.Message):
    temperature, feels_like = await weather.get_wheather()
    await msg.answer(f"Сейчас температура: {round(temperature, 1)}\n Чувствуется как {round(feels_like, 1)}")
