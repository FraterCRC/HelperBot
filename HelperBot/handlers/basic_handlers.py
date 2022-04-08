import logging
from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel_handler(msg: types.Message, state=FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    logging.info("Canceling state {current_state}")

    await state.finish()
    await msg.reply("Cancelled", reply_markup=types.ReplyKeyboardRemove())


async def not_handled_message_handler(msg: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)

    markup.add("/weather")
    markup.add("/set_drug_helper")

    await msg.answer("Вы можете:\n Узнать погодку: /weather\n" +
                     "Настроить напоминалку: /set_drug_helper", reply_markup=markup)
