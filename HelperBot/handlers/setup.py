from .basic_handlers import *
from .weather_handlers import *
from .drug_helper_handlers import DrugHelper
from aiogram import Dispatcher
from utils.time_dispatcher import TimeDispatcher
from .drug_helper_handlers import Form
from aiogram.dispatcher import filters
from .notification_handlers import NotificationHandlers


def setup_handlers(dp: Dispatcher, time_dp: TimeDispatcher):
    drug_handlers = DrugHelper(time_dp)
    notification_handlers = NotificationHandlers(time_dp)

    dp.register_message_handler(handleWeather, commands=["weather"])

    dp.register_message_handler(notification_handlers.handle_notification, 
        regexp='(2[0-3]|[01]?[0-9]):?([0-5]?[0-9])*')

    dp.register_message_handler(
        DrugHelper.start_drug_helper, commands=["set_drug_helper"])
    dp.register_message_handler(cancel_handler, state="*", commands=["cancel"])
    dp.register_message_handler(DrugHelper.procedd_day_part_invalid, lambda message: message.text not in [
                                "Утро", "День", "Вечер"], state=Form.day_part)
    dp.register_message_handler(
        DrugHelper.process_day_part, state=Form.day_part)
    dp.register_message_handler(
        drug_handlers.process_drug_name, state=Form.drug_name)

    dp.register_message_handler(not_handled_message_handler)
