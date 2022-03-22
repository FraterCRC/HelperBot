from ast import Call
import asyncio
from typing import Callable, Dict
import pytz
from datetime import datetime
from datetime import time
import json
import pathlib
import logging

class timeDispatcher():
    
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
            self.users.update({str(user["id"]): [(str(drug_name), str(day_part))]})
        self.save_users(pathlib.Path("user_data.json"))
      
    def save_users(self, path: pathlib.Path):
        print(self.users)
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
        await self.__updating()
        
    async def send_drug_reminder(self, user, drug_name):
        await self.bot.send_message(int(user), f"Не забудьте выпить {drug_name}", disable_notification=False)        
            
    async def __updating(self):
        print("HERE")
        while self.__is_updating:
            timezone = pytz.timezone("Etc/GMT-5")
            current_time = datetime.now(timezone)
            
            if current_time.time() > time(20):
                await self.update("Вечер")
                await asyncio.sleep(21600)
            elif current_time.time() > time(14):
                await self.update("День")
                await asyncio.sleep(21600)
            elif current_time.time() > time(8):
                await self.update("Утро")
                await asyncio.sleep(21600)
    async def update(self, day_part: str):
        print (len(self.users))
        if len(self.users) > 0:
            print("апдейчу")
            print(self.users)
            for key in self.users:
                for value in self.users[key]:
                    if str(value[1]) ==  day_part:
                        await self.send_drug_reminder(key, value[0])
        else:
            return 
                    
    async def time_handler(self, func: Callable) -> None:
        self.funcs.append(await func)

 
