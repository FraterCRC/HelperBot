from typing import Tuple
import aiohttp
from config import WHEATHER_TOKEN
import json
import logging


async def get_wheather() -> Tuple[float, float]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.openweathermap.org/data/2.5/weather", params={"q": "perm", "appid": WHEATHER_TOKEN}) as resp:
            logging.debug("weather:Make request: getWeather")
            data = await resp.text()
            data = json.loads(data)
            temperature = data['main']['temp'] - 273.15
            feels_like = data['main']['feels_like'] - 273.15
    return temperature, feels_like
