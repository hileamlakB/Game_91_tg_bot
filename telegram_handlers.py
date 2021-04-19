#!/usr/bin/env python3.8
"""
Telegram command handlers for the game_91 bot
"""
from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    pass


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message("@Ehm21", "talk to @Ehm21")
