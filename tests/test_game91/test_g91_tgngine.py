#!/usr/bin/env python3.8
"""
A test for the telegram test eninge, that playes the
game 91 game.
"""
import unittest
from game91.g91_tgngin import G91_tgngin

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot
from ptbtest import UserGenerator

from telegram.ext import CommandHandler, Updater


class G91_tg_ngin(unittest.TestCase):
    """Tests the game telegram engines with 2 userss"""
    def setup(self):

        # Prepare the basic mock tools and handlers
        self.bot = Mockbot()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispacther

        # create the engine to be tested
        self.engin = G91_tgngin()

        # Add the G91_tgngin's engin method as the message handler
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.ngine.engine))

        # Create two user for simulating users
        self.u1 = self.ug.get_user(first_name="User", last_name="1")
        self.u2 = self.ug.get_user(first_name="User", last_name="2")

        # Create a group chat and idividual chats with the two user for chat simulation
        self.gchat = self.cg.get_chat(type="supergroup")
        self.u1chat = self.cg.get_chat(user=u1)
        self.u2chat = self.cg.get_chat(user=u2)

    def test_create(self):
        """Tests the the create_game method of the
        tg_engine object"""

        self.updater.start_polling()
