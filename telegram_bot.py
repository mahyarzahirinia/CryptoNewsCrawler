from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


class NovncyBot:
    def __init__(self, token):
        """Start the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token("TOKEN").build()

        # on different commands - answer in Telegram
        # application.add_handler(CommandHandler("start", start))
        # application.add_handler(CommandHandler("help", help_command))

        # on non command i.e message - echo the message on Telegram
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)
