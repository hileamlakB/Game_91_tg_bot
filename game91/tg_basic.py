#!/usr/bin/env python3.8
"""
Telegram command handlers for the game_91 bot
"""
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    bot = context.bot
    bot.send_message(update.message.chat_id, "Bot is  up! Type !INS for more info")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message(update.message.chat_id, "Game 91 is a card game bot!! Glad you like to play! type !INS for instructions")
