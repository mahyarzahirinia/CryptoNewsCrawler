import asyncio
from telegram import Bot
from colorama import Fore, Style

from config import url
from telegram_bot import NovncyBot
from parser import Parser


async def main():
    try:
        engine = Parser(url=url, interval=70)
        await engine.get_update()

    except Exception as e:
        print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    asyncio.run(main())
