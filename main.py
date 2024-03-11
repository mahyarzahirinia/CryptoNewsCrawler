import asyncio
import sys
import traceback
import os

from colorama import Fore, Style

from parser import Parser
from dotenv import load_dotenv


async def main():
    try:
        if len(sys.argv) < 2:
            print("usage: python main.py [environment=development|production]")
            return

        environment = sys.argv[1]

        if environment == "development":
            dotenv_file = ".env.development"
        elif environment == "production":
            dotenv_file = ".env.production"
        else:
            print("Invalid environment specified. Use 'development' or 'production'.")
            return
        # load env
        load_dotenv(dotenv_file)

        # running the engine
        engine = Parser(url=os.getenv("URL"), interval=40, latest=3)
        await engine.get_update()

    except Exception as e:
        print(f"{Fore.RED}an Error occurred in the main: {e}{Style.RESET_ALL}")
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
