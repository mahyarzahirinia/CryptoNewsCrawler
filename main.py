# Crypto News Crawler
# this app is designed to crawl websites and extract
# crypto related information and rate them
import asyncio

from parser import Parser

from telegram_bot import NovncyBot


# from chatgpt_translation import initiate as initiate_gpt, translate


def main():
    # @cryptocrawler_novncy_bot
    telegram_token = '6852678484:AAGMa2Vt5yma_L2-NztGB_0XC7v1jGzeHW0'
    channel_id = '@cryptocrawler_novncy_bot'
    chatgpt_token = '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'
    chatgpt_token2 = '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'
    channel_id = '2052460067'
    url = 'https://coinmarketcap.com/headlines/news/'

    # try:
    #     init_bot(token=telegram_token)
    #     send_message(channel_id, 'testing')
    #
    # except Exception as e:
    #     print('exception happened on send_message')

    # Fetch and parse the website
    try:
        parser = Parser(url)
        news = parser.coinmarket_cap_stripper()
        print('success')
    except RuntimeError as e:
        print(e)

    # asyncio.run(run_telegram_bot(token=telegram_token, channel_id=channel_id))

    # try:
    #     initiate(telegram_token)
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # try:
    #     initiate_gpt(chatgpt_token2)
    #     translated = translate("I'm here to test something", 'persian')
    #     print(translated)
    # except Exception as e:
    #     print(f"An error occurred: {e}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
