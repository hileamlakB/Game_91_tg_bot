#!/usr/bin/env python3.8
"""
A test for the telegram test eninge, that playes the
game 91 game.
"""
import unittest
from game91.g91_tgngin import G91_tgingin
from game91.g91 import Game_91
from game91.g91_msgs import *
from card_games.cards import Cards

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]
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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]
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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]
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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

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
        self.u2chat = self.cg.get_chat(user=self.u2)

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

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

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR 12456", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        #[print(m) for m in self.bot.sent_messages]
        self.assertEqual(self.bot.sent_messages[-1]['text'], xgame_msg)

    @unittest.skip("No feature on the test suit to test this")
    def test_start_game_not_init(self):
        """Tests if the start functinoality of the game eninge works well
	    #this currently couldn't be tested due to the lack of such feature
	    in the ptbtest liberary. It doesn't have any restricution to whomm you
        may send a message
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        [print(m) for m in self.bot.sent_messages]
        #self.assertEqual(self.bot.sent_messages[-1]['text'], f'Player {user["first_name"]} hasn\'t initialized the bot\n')

    def test_start_game(self):
        """Tests if the start functinoality of the game eninge works well
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        #[print(m) for m in self.bot.sent_messages]

        self.assertEqual(self.bot.sent_messages[-1]['text'], "Make your round 1 bids!!")


class Test_BID(unittest.TestCase):
    """ Test the bid funcinality of the game engine object"""

    def __init__(self, *args, **kwargs):

        super(Test_BID, self).__init__(*args, **kwargs)

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
        self.users_cards = {user:Cards.CARD_VALUES[:] for user in self.users}
        self.u1 = self.ug.get_user(first_name="User", last_name="1", is_bot=False)
        self.u2 = self.ug.get_user(first_name="User", last_name="2", is_bot=False)

        # Create a group chat and idividual chats with the two user for chat simulation
        self.gchat = self.cg.get_chat(type="supergroup", title="game_91_test_bot", username="g91bot_tester")
        self.u2chat = self.cg.get_chat(user=self.u2)

    def setUp(self):
        self.updater.start_polling()

    def tearDown(self):
        self.updater.stop()

    def test_bid_no_value(self):
        """Tests if the start functinoality of the game eninge works well
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID", user=self.users[0])
        #[print(m) for m in self.bot.sent_messages]
        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], nbid_msg)

    def test_bid_rong_player(self):
        """Tests if bid functionality of the game properly handles
        wrong players
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID 3", user=self.u2)# u2 isn't part of the game
        #[print(m) for m in self.bot.sent_messages]
        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], xplay_msg)

    def test_bid_rong_type(self):
        """Tests if bid commad is used with the wrong kind of value
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID o", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], "Use a proper card value")


    def test_bid(self):
        """Tests if bid commad works for the correct case
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID 3", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

    def test_bid_chars(self):
        """Tests if bid commad works for the correct case wnen the cards are not
        numberd cards
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID j", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

        bid_update = self.mg.get_message(text="!BID K", user=self.users[1])

        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

    def test_con_bid(self):
        """Tests if bid commad works when some one uses it
        consequitevly in one round
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID 3", user=self.users[0])
        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        bid_update = self.mg.get_message(text="!BID 2", user=self.users[0])
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xconb_msg)

    def test_next_round(self):
        """Tests if it moves to the next round once
        everyone finishes bidding
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bids_msg = ""
        for user in self.users:
            bid_update =  self.mg.get_message(text="!BID 3", user=user)
            bids_msg += f"{user.first_name} bid 3\n"
            self.bot.insertUpdate(bid_update)


        self.assertEqual(self.bot.sent_messages[-1]['text'], bid_msg.format(2))
        self.assertTrue(self.bot.sent_messages[-2 - len(self.users)]['photo'] != '')

        texts = [x["text"] for x in self.bot.sent_messages if "text" in x]

        self.assertTrue("Here are round 1 prizes" in texts)
        self.assertTrue("Here are round 2 prizes" in texts)

        self.assertTrue(tie_msg in texts)
        self.assertTrue(bids_msg in texts)

    def test_bid_rong_card(self):
        """Tests if using a card twine for biding
        is handled
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        for user in self.users:
            bid_update =  self.mg.get_message(text="!BID 3", user=user)
            self.bot.insertUpdate(bid_update)

        bid_update = self.mg.get_message(text="!BID 3", user=self.users[0])
        self.bot.insertUpdate(bid_update)
        #print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], xcard_msg)

    def test_bid_post_round(self):
        """Test if round results are posted in during bidding
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)


        for user in self.users[:-1]:
            bid_update =  self.mg.get_message(text="!BID 2", user=user)
            self.bot.insertUpdate(bid_update)

        bid_update =  self.mg.get_message(text="!BID 3", user=self.users[-1])
        self.bot.insertUpdate(bid_update)

        texts = [x["text"] for x in self.bot.sent_messages if "text" in x]

        self.assertTrue(f"{self.users[-1].first_name} won this round" in texts)


    def test_bid_post_final(self):
        """Test if round results are posted in during bidding
        """

        crt_update = self.mg.get_message(text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, "Game Id: \w{4}")

        game_id = re.findall("Game Id: \w{4}", crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        def is_complete():
            """
            checks if the game is complete by checking all the users
            cards
            """
            #[print(cards) for _, cards in self.users_cards.items()]
            return all([not bool(len(cards)) for _, cards in self.users_cards.items()])


        # this only checks the integrity of the bot, doesn't check
        # the logic of the game calucaltion by itself so the classes
        # in charge of that should be tested on their own
        # run a sample game
        import random
        while not is_complete():
            for user in self.users:
                bid_card = random.choice(self.users_cards[user])
                self.users_cards[user].remove(bid_card)

                bid_update =  self.mg.get_message(text=f"!BID {bid_card}", user=user)
                self.bot.insertUpdate(bid_update)

        #print(self.bot.sent_messages[-1]["text"])
        self.assertRegex(self.bot.sent_messages[-1]["text"], "(No one won!! There was a tie)|(Congratulation)")
        #self.assertEqual(self.bot.sent_messages[-1], f"{self.users[-1].first_name} won this round")




if __name__ == "__main__":
    unittest.main()
