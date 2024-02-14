from telegram import Bot
from telegram.error import TelegramError
import time

bot = None


def init_bot(token):
    global bot
    bot = Bot(token)
    return bot
