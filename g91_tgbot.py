#!/usr/bin/env python3.8
"""
This script will start the telegram bot
that facilitates the game play of game-91
"""
import logging
import os

from game91.g91_tgngin import G91_tgingin
from game91.tg_basic import help_command, start
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

# Enable logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format,
                    level=logging.INFO,
                    filename="tg_bot.log")
# set up a listening port
PORT = int(os.environ.get('PORT', 5000))
TOKEN = "1622385036:AAHWRqkTwjUyFRvq8zb1iL7h3_uxqgedDeU"


def main() -> None:
    """Call this method to the start the bot."""

    # create a telegram `game 91` game_engine
    g_engine = G91_tgingin()

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOEKN,
                      use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, g_engine.engine))

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
