import asyncio
from telegram import Bot
from colorama import Fore, Style

from telegram_bot import NovncyBot


async def main():
    bot_name = '@cryptocrawler_novncy_bot'
    bot_token = '6852678484:AAGMa2Vt5yma_L2-NztGB_0XC7v1jGzeHW0'
    channel_name = '@test_novncy_bot_api'
    channel_id = '2052460067'
    url = 'https://coinmarketcap.com/headlines/news/'
    chatgpt_token = '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'
    chatgpt_token2 = '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'

    try:
        bot = NovncyBot(token=bot_token)
        await bot.send_message(channel_name=channel_name, message="testing again2")
    except Exception as e:
        print(f"{Fore.RED}Error sending message: {e}{Style.RESET_ALL}")

    # Fetch and parse the website
    try:
        # Uncomment this section once Parser class is defined
        # parser = Parser(url)
        # news = parser.coinmarket_cap_stripper()
        print('Website parsing and news extraction success')
    except RuntimeError as e:
        print(f"{Fore.RED}Error parsing website: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    asyncio.run(main())
