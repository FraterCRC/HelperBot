from aiogram import types


class NotificationHandlers():
    def __init__(self, time_dp) -> None:
        self.time_dp = time_dp
    async def handle_notification(self, msg: types.Message):
        self.time_dp.add_notification(msg.from_user, msg.text)
        await msg.answer("крута")