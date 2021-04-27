#!/usr/bin/env python3.8
"""
A test for the telegram test eninge, that playes the
game 91 game.
"""
import logging
import re
import unittest

from card_games.cards import Cards
from game91.g91 import Game_91
from game91.g91_msgs import (bid_msg, bids_msg, cmd_msg, ins_msg, maxp_msg,
                             nbid_msg, noid_msg, nstart_msg, ready_msg,
                             tie_msg, xaddp_msg, xcard_msg, xconb_msg,
                             xgame_msg, xplay_msg, xuser_msg, nid_msg,
                             xug_msg)
from game91.g91_tgngin import G91_tgingin
from ptbtest import ChatGenerator, MessageGenerator, Mockbot, UserGenerator
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

logging.getLogger(__name__).addHandler(logging.NullHandler())


class CommonInit(unittest.TestCase):
    """Defines all the common tools
    all the tests in this file use in its __init__ method"""

    def __init__(self, *args, **kwargs):
        super(CommonInit, self).__init__(*args, **kwargs)

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
        self.dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, self.engin.engine))

        # add a context
        self.context = CallbackContext(self.dispatcher)

        # Create users for simulating users
        self.users = [self.ug.get_user(is_bot=False)
                      for _ in range(Game_91.MAX_PLAYERS)]

        self.users_cards = {user: Cards.CARD_VALUES[:]
                            for user in self.users}
        self.u1 = self.ug.get_user(
            first_name="User", last_name="1", is_bot=False)
        self.u2 = self.ug.get_user(
            first_name="User", last_name="2", is_bot=False)

        # Create a group chat and idividual chats with the two user
        # for chat simulation
        self.gchat = self.cg.get_chat(
            type="supergroup", title="game_91_test_bot",
            username="g91bot_tester")
        self.gchat2 = self.cg.get_chat(
            type="supergroup", title="game_91_test_bot2",
            username="g91bot_tester2")
        self.gchat3 = self.cg.get_chat(
            type="supergroup", title="game_91_test_bot3",
            username="g91bot_tester3")
        self.u1chat = self.cg.get_chat(user=self.u1)
        self.u2chat = self.cg.get_chat(user=self.u2)

    def setUp(self):
        self.updater.start_polling()

    def tearDown(self):
        self.updater.stop()

    def create(self, chat, user) -> str:
        """
        Sends the create command (!CRT) to a bot and returns
        the response

        !this function is excpected to be called ufter
        updater.start_polling() and it is the callers
        responsibilty run updater.stop() after the
        call.
        """

        msg = self.mg.get_message(text="!CRT", chat=chat, user=user)
        self.bot.insertUpdate(msg)

        response = self.bot.sent_messages[-1]['text']
        return response


class Test_CRTnADD(CommonInit):
    """Tests the game telegram engines with 2 methods (CRT, ADD)"""

    def test_create(self):
        """Tests the the create_game method of the
        tg_engine object"""

        response = self.create(chat=self.gchat, user=self.u1)
        self.assertRegex(response, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

    def test_create_multi_chat(self):
        """Tests multiple game creation in the diferent group"""

        response = self.create(chat=self.gchat, user=self.u1)]
        self.assertRegex(response, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        response = self.create(chat=self.gchat2, user=self.u2)]
        self.assertRegex(response, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        self.assertRegex(recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        update3 = self.mg.get_message(
            text="!CRT", chat=self.gchat3, user=self.u1)
        self.bot.insertUpdate(update3)
        recieved = self.bot.sent_messages[0]['text']

        self.assertRegex(recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

    def test_multi_create(self):
        """Tests multiple gae creation in the same group"""

        for x in range(5):
            update = self.mg.get_message(
                text="!CRT", chat=self.gchat,
                user=self.u1)
            self.bot.insertUpdate(update)
            recieved = self.bot.sent_messages[-1]['text']

            self.assertRegex(recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")


    def test_add_no_id(self):
        """Tests the add player functinoality when
        no id is provided"""
        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        add_update = self.mg.get_message(text="!ADD",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], noid_msg)

    def test_add_wrong_id(self):
        """Tests the add player functinoality when
        no id is provided"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        add_update = self.mg.get_message(text="!ADD rongopokol",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], xgame_msg)

    def test_add(self):
        """Tests the add player functinoality of of the
        game 91 game engine"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        add_update = self.mg.get_message(text=f'!ADD {game_id}',
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[1]['text'], "User added!!")

    def test_player_already_added(self):
        """Checks if the correct message is sent if
        the same user trys to apply twice"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for x in range(2):
            add_update = self.mg.get_message(text=f"!ADD {game_id}",
                                             chat=self.gchat, user=self.u1)
            self.bot.insertUpdate(add_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'],
                         f"{self.u1.first_name} is already added!")

    def test_min_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MIN_PLAYERS):
            user = self.ug.get_user(is_bot=False)
            add_update = self.mg.get_message(text=f"!ADD {game_id}",
                                             chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)
            self.assertEqual(self.bot.sent_messages[1 + x]['text'],
                             f"{user.first_name} added!!")

        self.assertEqual(self.bot.sent_messages[-1]["text"], ready_msg)

    def test_max_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MAX_PLAYERS + 1):
            user = self.ug.get_user(is_bot=False)
            add_update = self.mg.get_message(text=f"!ADD {game_id}",
                                             chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        self.assertEqual(self.bot.sent_messages[-1]["text"], maxp_msg)

    def test_add_multi_game(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']

        game_id1 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[-1][-Game_91.ID_LENGTH:]

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[-1]['text']

        game_id2 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MIN_PLAYERS - 1):
            user = self.ug.get_user(is_bot=False)
            add_update = self.mg.get_message(text=f"!ADD {game_id1}",
                                             chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)
            self.assertRegex(self.bot.sent_messages[-1]["text"], f"{user.first_name} added!!")

            add_update2 = self.mg.get_message(text=f"!ADD {game_id2}",
                                             chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update2)

            self.assertRegex(self.bot.sent_messages[-1]["text"], f"{user.first_name} added!!")

    def test_add_multi_chat(self):
        """Tests multiple game creation in the diferent group"""

        update1 = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(update1)
        recieved = self.bot.sent_messages[-1]['text']
        game_id1 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             recieved)[0][-Game_91.ID_LENGTH:]


        add_update = self.mg.get_message(text=f"!ADD {game_id1}",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[-1]['text'], "User added!!")

        update2 = self.mg.get_message(
            text="!CRT", chat=self.gchat2, user=self.u2)
        self.bot.insertUpdate(update2)
        recieved = self.bot.sent_messages[-1]['text']
        game_id2 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             recieved)[0][-Game_91.ID_LENGTH:]


        add_update = self.mg.get_message(text=f"!ADD {game_id2}",
                                         chat=self.gchat2, user=self.u2)
        self.bot.insertUpdate(add_update)
        self.assertRegex(self.bot.sent_messages[-1]['text'], "User added!!")





class Test_STR(CommonInit):
    """Tests the start functinality of the tg game 91 eninge
    The command that will be tested is !STR"""

    def test_start_game_no_id(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(text=f"!ADD {game_id}",
                                             chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text="!STR",
                                         chat=self.gchat,
                                         user=self.u2)
        self.bot.insertUpdate(str_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], noid_msg)

    def test_start_game_not_ready(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat,
                                         user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        add_update = self.mg.get_message(text=f"!ADD {game_id}",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(text=f"!STR {game_id}",
                                         chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], nstart_msg)

    def test_start_game_wrong_id(self):
        """Tests if the start functinoality of the game eninge works well
        when a wrong id is used"""

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text="!STR 12456", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xgame_msg)

    @unittest.skip("No feature on the test suit to test this")
    def test_start_game_not_init(self):
        """Tests if the start functinoality of the game eninge works well
        this currently couldn't be tested due to the lack of such feature
        in the ptbtest liberary. It doesn't have any restricution to whom you
        may send a message
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)

        self.bot.insertUpdate(str_update)

        # once started check if some users are unautherized and  if the bot
        # reacted to that
        self.assertRegex(self.bot.sent_message[-1]["text"], xuser_msg)

        [print(m) for m in self.bot.sent_messages]

    def test_start_after_min_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        crt_update = self.mg.get_message(text="!CRT",
                                         chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             crt_recieved)[0][-Game_91.ID_LENGTH:]

        for user in self.users[:Game_91.MIN_PLAYERS]:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)
        self.assertEqual(self.bot.sent_messages[-1]["text"], ready_msg)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        self.assertEqual(
            self.bot.sent_messages[-1]['text'], "Make your round 1 bids!!")

    def test_start_game(self):
        """Tests if the start functinoality of the game eninge works well
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        self.assertEqual(
            self.bot.sent_messages[-1]['text'], "Make your round 1 bids!!")

    def test_add_after_start(self):
        """Tests if the start functinoality of the game eninge works well
        when some one tries to add a player after the game has started
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        add_update = self.mg.get_message(
            text=f"!ADD {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(add_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xaddp_msg)


class Test_BID(CommonInit):
    """ Test the bid funcinality of the game engine object"""

    def test_bid_no_value(self):
        """Tests if the start functinoality of the game eninge works well
        when there is no bid value
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID", user=self.users[0])
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], nbid_msg)

    def test_bid_no_id(self):
        """Tests if the start functinoality of the game eninge works well
        when there is no game id
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text="!BID 3", user=self.users[0])
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], nid_msg)

    def test_bid_rong_player(self):
        """Tests if bid functionality of the game properly handles
        wrong players (plaayers that didn't register)
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        # u2 is a unrigisterd player
        bid_update = self.mg.get_message(
            text=f"!BID 3 {game_id}", user=self.u2)
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xplay_msg)

    def test_bid_game_id(self):
        """Tests if bid functionality of the game properly handles
        wrong players (plaayers that didn't register)
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)


        bid_update = self.mg.get_message(
            text=f"!BID 3 wrongid", user=user, chat=self.u1chat)
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xug_msg)


    def test_bid_rong_type(self):
        """Tests if bid commad is used with the wrong kind of value
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text=f"!BID o {game_id}", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(
            self.bot.sent_messages[-1]['text'], "Use a proper card value")

    def test_bid(self):
        """Tests if bid commad works for the correct case
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=self.users[0])

        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

    def test_bid_chars(self):
        """Tests if bid commad works for the correct case wnen the cards
        are not numberd cards
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text=f"!BID j {game_id}", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

        bid_update = self.mg.get_message(text=f"!BID K {game_id}", user=self.users[1])

        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

    def test_con_bid(self):
        """Tests if bid commad works when some one uses it
        consequitevly in one round
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=self.users[0])
        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        bid_update = self.mg.get_message(text=f"!BID 2 {game_id}", user=self.users[0])
        self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], xconb_msg)

    def test_next_round(self):
        """Tests if it moves to the next round once
        everyone finishes bidding
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        bids_msg = ""
        for user in self.users:
            bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=user)
            bids_msg += f"{user.first_name} bid 3\n"
            self.bot.insertUpdate(bid_update)

        self.assertEqual(self.bot.sent_messages[-1]['text'], bid_msg.format(2))
        self.assertTrue(
            self.bot.sent_messages[-2 - len(self.users)]['photo'] != '')

        texts = [x["text"] for x in self.bot.sent_messages if "text" in x]

        self.assertTrue("Here are round 1 prizes" in texts)
        self.assertTrue("Here are round 2 prizes" in texts)

        self.assertTrue(tie_msg in texts)
        self.assertTrue(bids_msg in texts)

    def test_bid_rong_card(self):
        """Tests if using a card twine for biding
        is handled
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        for user in self.users:
            bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=user)
            self.bot.insertUpdate(bid_update)

        bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=self.users[0])
        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], xcard_msg)

    def test_bid_post_round(self):
        """Test if round results are posted in during bidding
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        for user in self.users[:-1]:
            bid_update = self.mg.get_message(text=f"!BID 2 {game_id}", user=user)
            self.bot.insertUpdate(bid_update)

        bid_update = self.mg.get_message(text=f"!BID 3 {game_id}", user=self.users[-1])
        self.bot.insertUpdate(bid_update)

        texts = [x["text"] for x in self.bot.sent_messages if "text" in x]

        self.assertTrue(f"{self.users[-1].first_name} won this round" in texts)

    def test_bid_post_final(self):
        """Test if round results are posted in during bidding
        """

        crt_update = self.mg.get_message(
            text="!CRT", chat=self.gchat, user=self.u1)
        self.bot.insertUpdate(crt_update)
        crt_recieved = self.bot.sent_messages[0]['text']
        self.assertRegex(crt_recieved, r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", crt_recieved)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            add_update = self.mg.get_message(
                text=f"!ADD {game_id}", chat=self.gchat, user=user)
            self.bot.insertUpdate(add_update)

        str_update = self.mg.get_message(
            text=f"!STR {game_id}", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(str_update)

        def is_complete():
            """
            checks if the game is complete by checking all the users
            cards
            """
            # [print(cards) for _, cards in self.users_cards.items()]
            return all([not bool(len(cards))
                        for _, cards in self.users_cards.items()])

        # !this only checks the integrity of the bot, doesn't check
        # !the logic of the game calucaltion by itself so the classes
        # !in charge of that should be tested on their own

        # run a sample game
        import random
        while not is_complete():
            for user in self.users:
                bid_card = random.choice(self.users_cards[user])
                self.users_cards[user].remove(bid_card)

                bid_update = self.mg.get_message(
                    text=f"!BID {bid_card} {game_id}", user=user)
                self.bot.insertUpdate(bid_update)

        # print(self.bot.sent_messages[-1]["text"])
        self.assertRegex(
            self.bot.sent_messages[-1]["text"],
            "(No one won!! There was a tie)|(Congratulation)")


class Test_CMDnINS(CommonInit):
    """ Test the CMD and INS funcinality of the game engine object"""

    def test_CMD(self):
        """Tests if the cmd functinoality of the game eninge works well
        in private chat
        """

        # on private chat
        cmd_update = self.mg.get_message(
            text="!CMD", chat=self.u2chat, user=self.u2)
        self.bot.insertUpdate(cmd_update)
        self.assertEqual(self.bot.sent_messages[-1]['text'], cmd_msg)

        # on group chat
        cmd_update = self.mg.get_message(
            text="!CMD", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(cmd_update)
        self.assertEqual(self.bot.sent_messages[-1]['text'], cmd_msg)

    def test_INS(self):
        """Tests if the cmd functinoality of the game eninge works well
        in private chat
        """

        # on private chat
        cmd_update = self.mg.get_message(
            text="!INS", chat=self.u2chat, user=self.u2)
        self.bot.insertUpdate(cmd_update)
        self.assertEqual(self.bot.sent_messages[-1]['text'], ins_msg)

        # on group chat
        cmd_update = self.mg.get_message(
            text="!INS", chat=self.gchat, user=self.u2)
        self.bot.insertUpdate(cmd_update)
        self.assertEqual(self.bot.sent_messages[-1]['text'], ins_msg)


if __name__ == "__main__":
    unittest.main()
