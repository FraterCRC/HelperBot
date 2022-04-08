import asyncio
from typing import Callable, Dict
from datetime import datetime
from datetime import time
import json
import pathlib
import logging
import sched
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class TimeDispatcher():

    def __init__(self, bot):
        self.__is_updating = False
        self.funcs = []
        self.bot = bot
        self.users = self.read_users(pathlib.Path("user_data.json"))
        if self.users == None:
            self.users = {}

    def add_user_drug(self, user, drug_name, day_part):
        if str(user["id"]) in self.users.keys():
            self.users[str(user["id"])].append([drug_name, day_part])
        else:
            self.users.update(
                {str(user["id"]): [(str(drug_name), str(day_part))]})
        self.save_users(pathlib.Path("user_data.json"))

    def save_users(self, path: pathlib.Path):
        with path.open('w') as f:
            logging.info("time_dispatcher: Saving user data")
            return json.dump(self.users, f, indent=4)

    def read_users(self, path: pathlib.Path):
        try:
            logging.info("time_dispatcher: Loading user data")
            with path.open('r') as f:
                return json.load(f)
        except FileNotFoundError:
            pass

    async def start_updating(self):
        self.__is_updating = True
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.update_day, trigger='cron',
                          hour=14, minute=0, second=0)
        scheduler.add_job(self.update_morning, trigger='cron',
                          hour=10, minute=0, second=0)
        scheduler.add_job(self.update_evening, trigger='cron',
                          hour=20, minute=22, second=0)
        scheduler.start()

    async def update_day(self):
        for key in self.users:
            for value in self.users[key]:
                if str(value[1]) == "День":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)

    async def update_evening(self):
        for key in self.users:
            for value in self.users[key]:
                if str(value[1]) == "Вечер":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)

    async def update_morning(self):
        for key in self.users:
            for value in self.users[key]:
                if str(value[1]) == "Утро":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)
