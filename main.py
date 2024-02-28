import asyncio

from colorama import Fore, Style

from parser import Parser
from dotenv import load_dotenv
import os

load_dotenv()


async def main():
    try:
        engine = Parser(url=os.getenv("URL"), interval=70, latest=1)
        await engine.get_update()

    except Exception as e:
        print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    asyncio.run(main())
