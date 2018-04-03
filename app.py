#small echo bot for Telegram

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#some useful constants
VERSION = os.getenv("OPENSHIFT_BUILD_NAME")
SOURCE = os.getenv("OPENSHIFT_BUILD_SOURCE")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("I'm a bot, please talk to me!")

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def fun(bot, update):
    """Send a message when the command /fun is issued."""
    chat_id = update.message.chat_id
    #bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    logger.info('User wants some fun in update %s',update)
    update.message.reply_text('fun function is not implemented yet :(')

def about(bot, update):
    """Information about current instance"""
    logger.info('User wants some info in update %s',update)
    update.message.reply_text('build version is '+VERSION)
    update.message.reply_text('running in OpenShift POD '+os.getenv("HOSTNAME"))
    update.message.reply_text('built from '+SOURCE)

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    TOKEN = os.getenv("BOT_CONFIG_token")
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("fun", fun))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("info", about))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main()
