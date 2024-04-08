import os

import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from colorama import Fore, Style


class NovncyBot:
    def __init__(self):
        self.application = None
        self.news_interval = int(os.getenv("INITIAL_NEWS_FETCH_INTERVAL"))
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))
        self.START, self.STOP, self.CHANGE_DURATION, self.INVITE = range(4)
        self.keyboard_options = [['Start', 'Stop'], ['Change Duration', 'Invite']]

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        await update.message.reply_text("Hi!")

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        menu = ("start: starts the bot to post news"
                "stop: stops the bot to post news"
                "set_interval: sets the bot interval")
        await update.message.reply_text(menu)

    async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the inline query. This is run when you type: @botusername <query>"""
        query = update.inline_query.query

        if not query:  # empty query should not be handled
            return

        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Caps",
                input_message_content=InputTextMessageContent(query.upper()),
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Bold",
                input_message_content=InputTextMessageContent(
                    f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
                ),
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Italic",
                input_message_content=InputTextMessageContent(
                    f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
                ),
            ),
        ]

        await update.inline_query.answer(results)

    async def send_with_message(self, channel_name: str, message: str):
        try:
            print(f"{Fore.CYAN}-posting on telegram{Style.RESET_ALL}")
            await self.bot.send_message(chat_id=channel_name, text=message, parse_mode=ParseMode.HTML)
            print(f"{Fore.GREEN}+posting done{Style.RESET_ALL}")
        except TelegramError as e:
            raise Exception(f"{Fore.RED}telegram: {e}{Style.RESET_ALL}")

    async def send_with_image(self, channel_name: str, image_url: str, message: str):
        try:
            print(f"{Fore.CYAN}-posting on telegram{Style.RESET_ALL}")
            await self.bot.send_photo(chat_id=channel_name, photo=image_url,
                                      caption=message, parse_mode=ParseMode.HTML)
            print(f"{Fore.GREEN}+posting done{Style.RESET_ALL}")
        except TelegramError as e:
            print(f"{Fore.RED}telegram: {e}{Style.RESET_ALL}")
            return

    async def get_message(self, channel_name: str):
        updates = await self.bot.get_updates(chat_id=channel_name, limit=1)
        if updates:
            last_message = updates[-1].message.text
            return last_message
        return None

    @property
    def news_interval(self):
        return self.news_interval

    @news_interval.setter
    def news_interval(self, value):
        if value > 0:
            self.radius = value

    def run_interactive(self):
        # Create the application using builder pattern
        self.application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

        # Add handlers for commands/messages
        self.application.add_handler(CommandHandler("start", self.start))

        # Start the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
