import telegram
from telegram import Bot
from telegram.constants import ParseMode


class NovncyBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send_message(self, channel_name: str, message: str):
        await self.bot.send_message(chat_id=channel_name, text=message, parse_mode=ParseMode.HTML)

    async def send_image(self, channel_name: str, image_url: str, message: str):
        await self.bot.send_photo(chat_id=channel_name, photo=image_url, caption=message, parse_mode=ParseMode.HTML)
