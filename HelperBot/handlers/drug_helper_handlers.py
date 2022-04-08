from pathlib import Path
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.files import JSONStorage


class Form(StatesGroup):
    day_part = State()
    drug_name = State()


class DrugHelper():
    def __init__(self, time_dp) -> None:
        self.time_dp = time_dp

    async def start_drug_helper(msg: types.Message, state: FSMContext):
        await Form.day_part.set()

        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, selective=True)
        markup.add("Утро")
        markup.add("День")
        markup.add("Вечер")

        await msg.reply("Введите, когда принимать таблетки(утро,день,вечер).", reply_markup=markup)

    async def procedd_day_part_invalid(msg: types.Message, state: FSMContext):
        return await msg.reply("Используйте кнопочки.")

    async def process_day_part(msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["day_part"] = msg.text

            markup = types.ReplyKeyboardRemove()

            await msg.reply("Введите название лекарства", reply_markup=markup)
            await Form.next()
        state.storage.write(Path("data.json"))

    async def process_drug_name(self, msg: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data["drug_name"] = msg.text
            self.time_dp.add_user_drug(
                msg.from_user, data["drug_name"], data["day_part"])
        await state.finish()
        await msg.reply("Спасибо!")
        state.storage.write(Path("data.json"))
