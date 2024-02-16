import telegram
from telegram import Bot


class NovncyBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send_message(self, channel_name: str, message: str):
        await self.bot.send_message(chat_id=channel_name, text=message)
