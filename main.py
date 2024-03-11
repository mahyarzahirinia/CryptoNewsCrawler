import asyncio
import traceback

from colorama import Fore, Style

from parser import Parser
from dotenv import load_dotenv
import os

load_dotenv('.env.development')


async def main():
    try:
        engine = Parser(url=os.getenv("URL"), interval=20, latest=3)
        await engine.get_update()

    except Exception as e:
        print(f"{Fore.RED}an Error occurred in the main: {e}{Style.RESET_ALL}")
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
