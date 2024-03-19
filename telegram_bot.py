import os

import telegram
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from colorama import Fore, Style


class NovncyBot:
    def __init__(self):
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))

    async def send_message(self, channel_name: str, message: str):
        try:
            print(f"{Fore.CYAN}-posting on telegram{Style.RESET_ALL}")
            await self.bot.send_message(chat_id=channel_name, text=message, parse_mode=ParseMode.HTML)
            print(f"{Fore.GREEN}+posting done{Style.RESET_ALL}")
        except TelegramError as e:
            raise Exception(f"{Fore.RED}telegram: {e}{Style.RESET_ALL}")

    async def send_image(self, channel_name: str, image_url: str, message: str):
        try:
            print(f"{Fore.CYAN}-posting on telegram{Style.RESET_ALL}")
            await self.bot.send_photo(chat_id=channel_name, photo=image_url,
                                      caption=message, parse_mode=ParseMode.HTML)
            print(f"{Fore.GREEN}+posting done{Style.RESET_ALL}")
        except TelegramError as e:
            raise Exception(f"{Fore.RED}telegram: {e}{Style.RESET_ALL}")
        finally:
            return

    async def get_message(self, channel_name: str):
        updates = await self.bot.get_updates(chat_id=channel_name, limit=1)
        if updates:
            last_message = updates[-1].message.text
            return last_message
        return None
