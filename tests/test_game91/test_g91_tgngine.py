#!/usr/bin/env python3.8
"""
A test for the telegram test eninge, that playes the
game 91 game.
"""
import unittest
from game91.g91_tgngin import G91_tgingin
from game91.g91 import Game_91
from game91.g91_msgs import *

import logging
from telegram.ext import CommandHandler, Updater, Filters, CallbackContext, MessageHandler
from ptbtest import *

import re

#log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#logging.basicConfig(format=log_format, level=logging.INFO)

logging.getLogger(__name__).addHandler(logging.NullHandler())

class Test_CRTnADD(unittest.TestCase):
    """Tests the game telegram engines with 2 methods (CRT, ADD)"""

    def __init__(self, *args, **kwargs):

        super(Test_CRTnADD, self).__init__(*args, **kwargs)

         # Prepare the basic mock tools and handlers
        self.bot = Mockbot()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        self.mg = MessageGenerator()
        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher

        # create the engine to be tested
        self.engin = G91_tgingin()

        # Add the G91_tgngin's engin method as the message handler
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.engin.engine))

        # add a context
        self.context = CallbackContext(self.dispatcher)

        # Create two user for simulating users
        self.u1 = self.ug.get_user(first_name="User", last_name="1", is_bot=False)
        self.u2 = self.ug.get_user(first_name="User", last_name="2", is_bot=False)

        # Create a group chat and idividual chats with the two user for chat simulation
        self.gchat = self.cg.get_chat(type="supergroup", title="game_91_test_bot", username="g91bot_tester")
        self.u1chat = self.cg.get_chat(user=self.u1)
        self.u2chat = self.cg.get_chat(user=self.u2)

    def setUp(self):
        self.updater.start_polling()

    def tearDown(self):
        self.updater.stop()

    def test_create(self):
        """Tests the the create_game method of the
        tg_engine object"""

        update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(update)
        recieved = self.bot.sent_messages[0]['text']

        self.assertRegex(recieved, "Game Id: \w{4}")

    def test_add_no_id(self):
        """Tests the add player functinoality when
        no id is provided"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]
        add_update = self.mg.get_message(text=f"!ADD", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], noid_msg)


    def test_add_wrong_id(self):
        """Tests the add player functinoality when
        no id is provided"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]
        add_update = self.mg.get_message(text=f"!ADD rong", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], xgame_msg)

    def test_add(self):
        """Tests the add player functinoality of of the
        game 91 game engine"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]
        add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], "User added!!")


    def test_player_already_added(self):
        """Checks if the correct message is sent if
        the same user trys to apply twice"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for x in range(2):
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=self.u1)
            self.bot.insertUpdate(add_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], f"{self.u1.first_name} is already added!")


    def test_min_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for x in range(Game_91.MIN_PLAYERS):
            user = self.ug.get_user(is_bot=False)
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)
            self.assertEqual(self.bot.sent_messages[1 + x]['text'], f"{user.first_name} added!!")

        self.assertEqual(self.bot.sent_messages[-1]["text"], ready_msg)

    def test_max_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for x in range(Game_91.MAX_PLAYERS + 1):
            user = self.ug.get_user(is_bot=False)
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        self.assertEqual(self.bot.sent_messages[-1]["text"], maxp_msg)



class Test_STR(unittest.TestCase):
    """Tests the start functinality of the tg game 91 eninge
    The command that will be tested is !STR"""
    def __init__(self, *args, **kwargs):

        super(Test_STR, self).__init__(*args, **kwargs)

         # Prepare the basic mock tools and handlers
        self.bot = Mockbot()
        self.ug = UserGenerator()
        self.cg = ChatGenerator()
        self.mg = MessageGenerator()
        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher

        # create the engine to be tested
        self.engin = G91_tgingin()

        # Add the G91_tgngin's engin method as the message handler
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.engin.engine))

        # add a context
        self.context = CallbackContext(self.dispatcher)

        # Create two user for simulating users
        self.users = [self.ug.get_user(is_bot=False) for _ in range(Game_91.MAX_PLAYERS)]
        self.u1 = self.ug.get_user(first_name="User", last_name="1", is_bot=False)
        self.u2 = self.ug.get_user(first_name="User", last_name="2", is_bot=False)

        # Create a group chat and idividual chats with the two user for chat simulation
        self.gchat = self.cg.get_chat(type="supergroup", title="game_91_test_bot", username="g91bot_tester")

    def setUp(self):
        self.updater.start_polling()

    def tearDown(self):
        self.updater.stop()

    def test_start_game_no_id(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)


        str_update = self.mg.get_message(text=f"!STR", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)


        self.assertEqual(self.bot.sent_messages[-1]['text'], noid_msg)

    def test_start_game_not_ready(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]


        add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)


        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)


        self.assertEqual(self.bot.sent_messages[-1]['text'], nstart_msg)

    def test_start_game_wrong_id(self):
        """Tests if the start functinoality of the game eninge works well
        when a wrong id is used"""

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR 12456", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        #[print(m) for m in self.bot.sent_messages]
        self.assertEqual(self.bot.sent_messages[-1]['text'], xgame_msg)

    def test_start_game_not_init(self):
        """Tests if the start functinoality of the game eninge works well
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-4:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        [print(m) for m in self.bot.sent_messages]
        #self.assertEqual(self.bot.sent_messages[-1]['text'], f'Player {user["first_name"]} hasn\'t initialized the bot\n')
