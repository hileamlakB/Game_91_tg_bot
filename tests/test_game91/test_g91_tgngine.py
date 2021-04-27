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

    def send(self, cmd, chat=None, user=None, index=-1) -> str:
        """
        Sends the cmd command to the mock bot and returns
        the 'text' attribut of the last response

        !this function is excpected to be called after
        updater.start_polling() and it is the callers
        responsibilty run updater.stop() after the
        call.

        Atributes
            @cmd - The cmd to be send
            @chat - The chat object to which the message is sent
            @user - The user object who sends the message
            @index - the index of the response message to be send from the list
                    of messages sent by the bot. By default the latest
                    one will be sent
        """

        msg = self.mg.get_message(text=cmd, chat=chat, user=user)
        self.bot.insertUpdate(msg)

        if 'text' in self.bot.sent_messages[index]:
            response = self.bot.sent_messages[index]['text']
            return response
        return "'"


class Test_CRTnADD(CommonInit):
    """Tests the game telegram engines with 2 methods (CRT, ADD)"""

    def test_create(self):
        """Tests the the create_game method of the
        tg_engine object"""

        response = self.send("!CRT", self.gchat, self.u1)
        self.assertRegex(response,
                         r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

    def test_create_multi_chat(self):
        """Tests multiple game creation in the diferent group"""

        response = self.send("!CRT", self.gchat, self.u1)
        self.assertRegex(response,
                         r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        response = self.send("!CRT", self.gchat2, self.u2)
        self.assertRegex(response,
                         r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

        # one player in different group at the same time
        response = self.send("!CRT", self.gchat3, self.u1)
        self.assertRegex(response,
                         r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

    def test_multi_create(self):
        """Tests multiple gae creation in the same group"""

        # one player in one group
        # in multiple games
        for x in range(5):
            response = self.send("!CRT", self.gchat, self.u1)
            self.assertRegex(response,
                             r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}")

    def test_add_no_id(self):
        """Tests the add player functinoality when
        no id is provided"""

        self.send("!CRT", self.gchat, self.u1)
        response = self.send("!ADD", self.gchat, self.u1)
        self.assertRegex(response, noid_msg)

    def test_add_wrong_id(self):
        """Tests the add player functinoality when
        no id is provided"""

        self.send("!CRT", self.gchat, self.u1)
        response = self.send("!ADD rongopokol", self.gchat, self.u1)
        self.assertRegex(response, xgame_msg)

    def test_add(self):
        """Tests the add player functinoality of of the
        game 91 game engine"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        response = self.send(f'!ADD {game_id}', self.gchat, self.u1)
        self.assertRegex(response, "User added!!")

    def test_player_already_added(self):
        """Checks if the correct message is sent if
        the same user trys to apply twice"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        for x in range(2):
            response = self.send(f'!ADD {game_id}', self.gchat, self.u1)

        self.assertEqual(response, f"{self.u1.first_name} is already added!")

    def test_min_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MIN_PLAYERS):
            user = self.ug.get_user(is_bot=False)
            # index of 1 + x is used to get the exact response for
            # the request since there are clutter messages in between send
            # by the bot. And 1 is used, since there is alreay one message
            # from the creat command in the start
            response = self.send(f'!ADD {game_id}', self.gchat, user, 1 + x)
            self.assertEqual(response, f"{user.first_name} added!!")

        self.assertEqual(self.bot.sent_messages[-1]["text"], ready_msg)

    def test_max_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MAX_PLAYERS + 1):
            user = self.ug.get_user(is_bot=False)
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        self.assertEqual(response, maxp_msg)

    def test_add_multi_game(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id1 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                              response)[-1][-Game_91.ID_LENGTH:]

        response = self.send("!CRT", self.gchat, self.u1)
        game_id2 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                              response)[0][-Game_91.ID_LENGTH:]

        for x in range(Game_91.MIN_PLAYERS - 1):
            user = self.ug.get_user(is_bot=False)
            response = self.send(f'!ADD {game_id1}', self.gchat, user)
            self.assertRegex(response, f"{user.first_name} added!!")

            user = self.ug.get_user(is_bot=False)
            response = self.send(f'!ADD {game_id2}', self.gchat, user)
            self.assertRegex(response, f"{user.first_name} added!!")

    def test_add_multi_chat(self):
        """Tests multiple game creation in the diferent group"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id1 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                              response)[0][-Game_91.ID_LENGTH:]

        response = self.send(f'!ADD {game_id1}', self.gchat, self.u1)
        self.assertRegex(response, f"{self.u1.first_name} added!!")

        response = self.send("!CRT", self.gchat2, self.u2)
        game_id2 = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                              response)[0][-Game_91.ID_LENGTH:]

        response = self.send(f'!ADD {game_id2}', self.gchat2, self.u2)
        self.assertRegex(response, f"{self.u2.first_name} added!!")


class Test_STR(CommonInit):
    """Tests the start functinality of the tg game 91 eninge
    The command that will be tested is !STR"""

    def test_start_game_no_id(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send("!STR", self.gchat, self.u2)

        self.assertEqual(response, noid_msg)

    def test_start_game_not_ready(self):
        """Tests if the start functinoality of the game eninge works well
        when there are no id"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        self.send(f'!ADD {game_id}', self.gchat, self.u1)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)
        self.assertEqual(response, nstart_msg)

    def test_start_game_wrong_id(self):
        """Tests if the start functinoality of the game eninge works well
        when a wrong id is used"""

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send("!STR 12456", self.gchat, self.u2)

        self.assertEqual(response, xgame_msg)

    @unittest.skip("No feature on the test suit to test this")
    def test_start_game_not_init(self):
        """Tests if the start functinoality of the game eninge works well
        this currently couldn't be tested due to the lack of such feature
        in the ptbtest liberary. It doesn't have any restricution to whom you
        may send a message
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)

        # once started check if some users are unautherized and  if the bot
        # reacted to that
        self.assertRegex(response, xuser_msg)

        [print(m) for m in self.bot.sent_messages]

    def test_start_after_min_player_added(self):
        """Tests the add player functinoality of of the
        game 91 game engine, and check if the game will ask to
        start after the mimimum number of players"""

        response = self.send("!CRT", self.gchat, self.u1)
        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}",
                             response)[0][-Game_91.ID_LENGTH:]

        for user in self.users[:Game_91.MIN_PLAYERS]:
            response = self.send(f'!ADD {game_id}', self.gchat, user)
        self.assertEqual(self.bot.sent_messages[-1]["text"], ready_msg)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)

        self.assertEqual(
            self.bot.sent_messages[-1]['text'], "Make your round 1 bids!!")

    def test_start_game(self):
        """Tests if the start functinoality of the game eninge works well
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)

        self.assertEqual(response, "Make your round 1 bids!!")

    def test_add_after_start(self):
        """Tests if the start functinoality of the game eninge works well
        when some one tries to add a player after the game has started
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send(f"!ADD {game_id}", self.gchat, self.u2)

        self.assertEqual(response, xaddp_msg)


class Test_BID(CommonInit):
    """ Test the bid funcinality of the game engine object"""

    def test_bid_no_value(self):
        """Tests if the start functinoality of the game eninge works well
        when there is no bid value
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send("!BID", user=self.users[0])

        self.assertEqual(response, nbid_msg)

    def test_bid_no_id(self):
        """Tests if the start functinoality of the game eninge works well
        when there is no game id
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send("!BID 3", user=self.users[0])

        self.assertEqual(response, nid_msg)

    def test_bid_rong_player(self):
        """Tests if bid functionality of the game properly handles
        wrong players (plaayers that didn't register)
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        # u2 is a unrigisterd player
        response = self.send(cmd=f"!BID 3 {game_id}", user=self.u2)

        self.assertEqual(response, xplay_msg)

    def test_bid_game_id(self):
        """Tests if bid functionality of the game properly handles
        wrong players (plaayers that didn't register)
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send(cmd="!BID 3 wrongid", user=user)

        self.assertEqual(response, xug_msg)

    def test_bid_rong_type(self):
        """Tests if bid commad is used with the wrong kind of value
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send(cmd=f"!BID o {game_id}", user=self.users[0])

        self.assertEqual(response, "Use a proper card value")

    def test_bid(self):
        """Tests if bid commad works for the correct case
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        response = self.send(cmd=f"!BID 3 {game_id}", user=self.users[0])

        self.assertEqual(response, bids_msg)

    def test_bid_chars(self):
        """Tests if bid commad works for the correct case wnen the cards
        are not numberd cards
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            response = self.send(f'!ADD {game_id}', self.gchat, user)

        response = self.send(f"!STR {game_id}", self.gchat, self.u2)

        bid_update = self.mg.get_message(
            text=f"!BID j {game_id}", user=self.users[0])

        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

        bid_update = self.mg.get_message(
            text=f"!BID K {game_id}", user=self.users[1])

        self.bot.insertUpdate(bid_update)
        # print(self.bot.sent_messages[-1])

        self.assertEqual(self.bot.sent_messages[-1]['text'], bids_msg)

    def test_con_bid(self):
        """Tests if bid commad works when some one uses it
        consequitevly in one round
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        self.send(cmd=f"!BID 3 {game_id}", user=self.users[0])

        response = self.send(cmd=f"!BID 2 {game_id}", user=self.users[0])

        self.assertEqual(response, xconb_msg)

    def test_next_round(self):
        """Tests if it moves to the next round once
        everyone finishes bidding
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        bids_msg = ""
        for user in self.users:
            response = self.send(cmd=f"!BID 3 {game_id}", user=user)
            bids_msg += f"{user.first_name} bid 3\n"

        self.assertEqual(response, bid_msg.format(2))
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

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        for user in self.users:
            self.send(cmd=f"!BID 3 {game_id}", user=user)

        response = self.send(cmd=f"!BID 3 {game_id}", user=self.users[0])

        self.assertEqual(response, xcard_msg)

    def test_bid_post_round(self):
        """Test if round results are posted in during bidding
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

        for user in self.users[:-1]:
            self.send(cmd=f"!BID 2 {game_id}", user=user)

        response = self.send(cmd=f"!BID 3 {game_id}", user=self.users[-1])

        texts = [x["text"] for x in self.bot.sent_messages if "text" in x]

        self.assertTrue(f"{self.users[-1].first_name} won this round" in texts)

    def test_bid_post_final(self):
        """Test if round results are posted in during bidding
        """

        response = self.send("!CRT", self.gchat, self.u1)

        game_id = re.findall(r"Game Id: \w{" + str(Game_91.ID_LENGTH) + "}", response)[
            0][-Game_91.ID_LENGTH:]

        for user in self.users:
            self.send(f'!ADD {game_id}', self.gchat, user)

        self.send(f"!STR {game_id}", self.gchat, self.u2)

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

                response = self.send(
                    cmd=f"!BID {bid_card} {game_id}", user=user)

        # print(self.bot.sent_messages[-1]["text"])
        self.assertRegex(
            response,
            "(No one won!! There was a tie)|(Congratulation)")


class Test_CMDnINS(CommonInit):
    """ Test the CMD and INS funcinality of the game engine object"""

    def test_CMD(self):
        """Tests if the cmd functinoality of the game eninge works well
        in private chat
        """

        # on private chat
        response = self.send(cmd="!CMD", chat=self.u2chat, user=self.u2)
        self.assertEqual(response, cmd_msg)

        # on group chat
        response = self.send(cmd="!CMD", chat=self.gchat, user=self.u2)
        self.assertEqual(response, cmd_msg)

    def test_INS(self):
        """Tests if the cmd functinoality of the game eninge works well
        in private chat
        """

        # on private chat
        response = self.send(cmd="!INS", chat=self.u2chat, user=self.u2)
        self.assertEqual(response, ins_msg)

        # on group chat
        response = self.send(cmd="!INS", chat=self.gchat, user=self.u2)
        self.assertEqual(response, ins_msg)


if __name__ == "__main__":
    unittest.main()
