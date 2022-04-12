import asyncio
from typing import Callable, Dict
from datetime import datetime
from datetime import time
import json
import pathlib
import logging
import sched
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone


class TimeFunction():
    def __init__(self, job_name: str, bot, user, scheduler) -> None:
        self.job = job_name
        self.bot = bot
        self.scheduler = scheduler
        self.user = user

    async def remind(self):
        text = self.job[5:]
        await self.bot.send_message(int(self.user), f"Напоминаю: {text}", disable_notification=False)
        self.scheduler.remove_job(self.job)


class TimeDispatcher():

    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')
        self.drugs = self.__read_data(pathlib.Path("user_drugs.json"))
        self.notifications = self.__read_data(
            pathlib.Path("user_notifications.json"))
        if self.drugs == None:
            self.drugs = {}
        if self.notifications == None:
            self.notifications = {}

    def add_notification(self, user, text: str):
        time_func_class = TimeFunction(text, self.bot, user, self.scheduler)
        hours = text[:2]
        minutes = text[3:5]
        print(hours)
        print(minutes)
        self.scheduler.add_job(time_func_class.remind, trigger='cron',
                               hour=hours, minute=minutes, id=time_func_class.job)

    def add_user_drug(self, user, drug_name, day_part):
        if str(user["id"]) in self.drugs.keys():
            self.drugs[str(user["id"])].append([drug_name, day_part])
        else:
            self.drugs.update(
                {str(user["id"]): [(str(drug_name), str(day_part))]})
        self.__save_data(pathlib.Path("user_drugs.json"))

    def __save_data(self, path: pathlib.Path):
        with path.open('w') as f:
            logging.info("time_dispatcher: Saving user data")
            return json.dump(self.drugs, f, indent=4)

    def __read_data(self, path: pathlib.Path):
        try:
            logging.info("time_dispatcher: Loading user data")
            with path.open('r') as f:
                return json.load(f)
        except FileNotFoundError:
            pass

    async def start_updating(self):

        self.scheduler.add_job(self.update_day, trigger='cron',
                               hour=14, minute=0, second=0)
        self.scheduler.add_job(self.update_morning, trigger='cron',
                               hour=10, minute=0, second=0)
        self.scheduler.add_job(self.update_evening, trigger='cron',
                               hour=20, minute=22, second=0)
        self.scheduler.start()

    async def update_day(self):
        for key in self.drugs:
            for value in self.drugs[key]:
                if str(value[1]) == "День":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)

    async def update_evening(self):
        for key in self.drugs:
            for value in self.drugs[key]:
                if str(value[1]) == "Вечер":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)

    async def update_morning(self):
        for key in self.drugs:
            for value in self.drugs[key]:
                if str(value[1]) == "Утро":
                    await self.bot.send_message(int(key), f"Не забудьте выпить {value[0]}", disable_notification=False)
