#!/usr/bin/env python3.8
"""
This file defines a telegram game engine for
the game 91 card game
"""

from telegram import Update
from telegram.ext import  CallbackContext
from telegram.error import Unauthorized

from .g91 import Game_91
from .g91_msgs import *
from card_players.player import Player

class G91_tgingin:
    """
    A game_91 card game engine
    to run the game on a telegram bot
    """

    def __init__(self) -> None:
        """
        Creates an instance of a telegram game91
        game engine
        """

        # format
        # {COMAND: [[CHAT_TYPE, . . .], CALLBACK_FUNCTION]}
        self.cmd_map = {
        "!CRT" : [["group", "supergroup"], self.create_game],
        "!ADD" : [["group", "supergroup"], self.add_player],
        "!STR" : [["group", "supergroup"], self.start_game],
        "!BID" : [["private", "supergroup"], self.bid_card],
        "!INS" : [["group", "private", "supergroup"], self.show_ins],
        "!CMD" : [["group", "private", "supergroup"], self.show_cmd],
        }

        self.SUIT_OPTIONS = ["CLUB", "DIAMOND", "SPADE", "FLOWER"]
        self.current_option = 0

    def next_suit(self):
        """
        return the next unused suit
        """

        if self.current_option == 4:
            self.current_option = 0

        current = self.current_option
        self.current_option += 1
        return self.SUIT_OPTIONS[current]

    def req_bid(self, bot, group_id, game):
        """
        Sends a bid request including images to private and group messages
        """
        bot.send_message(group_id, f"Here are round {game.round} prizes")
        prizes = game.current_prize
        for prize in prizes:
            iname = str(prize[1]) + prize[0][0] + ".png"
            with open("./data/card_images/"+iname, 'rb') as im:
                bot.send_photo(group_id, photo=im.read(), caption=f"The {prize[1]} of {prize[0]} is up for a bid" )
        bot.send_message(group_id, bid_msg.format(game.round))

        for player in game.get_players():
            pid = player.user['id']
            bot.send_message(pid, bid_msg.format(game.round))

    def test_init(self, bot, game):
        """
        Checks if bot messaging is initialized with all players
        returns a list of all the players that haven't initialized bot chat.
        TODO
        See if there is a better way to check autherization without sening messages
        """
        uusers = []

        for player in game.get_players():
            try:
                pid = player.user['id']
                bot.send_message(pid, "TEST")

            except Unauthorized:
                uusers.append(player.user['first_name'])
        return uusers

    def req_init(self, bot, group_id, uusers):
        """
        requests users who haven't initalized to start converation with bot
        Takes a list of unauthorized users an the bot object
        """
        msg = xuser_msg + "\n"
        for user in uusers:
            msg += f"Player {user} hasn't initialized the bot\n"
        bot.send_message(group_id, msg)

    def check_bid(self, bot, user_id, game, player, bid):
        """
        Checks if a bid is correct, based on the rules, and the
        input from the player.

        If any test fail sends a pivate message to the bidder and returns False
        otherwise it returns True
        """
        try:
            bid_stat = game.add_bid(player, int(bid))
        except ValueError:
            bot.send_message(user_id, "Use a proper card value")
            return False

        if bid_stat == None:
            bot.send_message(user_id, "You can't bid now! wait till this round is over")
            return False

        if bid_stat == []:
            bot.send_message(user_id, "You can't bid with that card you don't have it")
            return False

        return True

    def post_round(self, bot, group_id, game):
        """
        Posts round end information, including who won the round
        """
        winner = game.handle_winner()
        if winner[0] != None:
            bot.send_message(group_id, f"{winner[0].name} won this round")
            return

        bot.send_message(group_id, tie_msg)

    def post_final(self, bot, group_id, game):
        """Poss the fnial message one the game is over"""
        f_winner = game.final_winner()
        if len(f_winner) == 1:
            bot.send_message(group_id, win_msg.format(f_winner[0].name, f_winner[0].total_points))
            return

        w_msg = "No one won!! There was a tie between "
        for winner in f_winner:
            w_msg += f"{winner.name}, "
        bot.send_message(group_id, w_msg)

    def create_game(self, update: Update, context: CallbackContext) -> None:
        """
        Ideally called when the !CRT command is inserted
        Creates a game object and stores it in the bot data
        """

        chat_id = update.message.chat_id
        bot = context.bot

        # check if no game object in this group before you
        # create a new object, to be impoved in the future
        if not context.chat_data:
            game = Game_91()

            game.chat_id = str(chat_id)

            context.chat_data[game.id] = game
            context.bot_data[chat_id] = game

            pmin = Game_91.MIN_PLAYERS
            pmax = Game_91.MAX_PLAYERS
            bot.send_message(chat_id, game_created.format(game.id, pmin, pmax))


    def add_player(self, update: Update, context: CallbackContext) -> None:
        """
        Adds a player to an already started game in the group
        using the id
        """

        cmd = update.message.text.split(" ")
        chat_id = update.message.chat_id
        bot = context.bot

        if len(cmd) < 2:
            bot.send_message(chat_id, noid_msg)
            return

        game_id = cmd[1]
        # check if the game id is in the group data
        if game_id not in context.chat_data:
            bot.send_message(chat_id, xgame_msg)
            return

        curent_game = context.chat_data[game_id]
        user = update.effective_user
        player = Player(user.first_name, curent_game, self.next_suit())
        player.user = user

        if user.id in context.bot_data:
            bot.send_message(chat_id, f"{user.first_name} is already added!")
            return

        if curent_game.is_started:
            bot.send_message(chat_id, xaddp_msg)
            return

        if not curent_game.add_player(player):
            bot.send_message(chat_id, maxp_msg)
            return
        bot.send_message(chat_id, f"{user.first_name} added!!")

        context.bot_data[user.id] = player
        if curent_game.is_ready():
            bot.send_message(chat_id, ready_msg)

    def start_game(self, update: Update, context: CallbackContext) -> None:
        """ Starts a game with a specified id """

        cmd = update.message.text.split(" ")
        chat_id = update.message.chat_id
        bot = context.bot

        if len(cmd) < 2:
            bot.send_message(chat_id, noid_msg)
            return

        game_id = cmd[1]
        if game_id not in context.chat_data:
             bot.send_message(chat_id, xgame_msg)
             return

        curent_game = context.chat_data[game_id]
        if curent_game.is_started:
            bot.send_message(chat_id, init_msg)
            return

        if curent_game.is_ready():
            # check if all the playrs have started bot messaging
            uusers = self.test_init(bot, curent_game)

            if not uusers:
                curent_game.start()
                bot.send_message(chat_id, started_msg)
                self.req_bid(bot, chat_id, curent_game)
            else:
                self.req_init(bot, chat_id, uusers)
        else:
            bot.send_message(chat_id, nstart_msg)

    def bid_card(self, update: Update, context: CallbackContext) -> None:
        """ Process bids from uses on private chat """
        bot = context.bot
        cmd = update.message.text.split(" ")

        user = update.effective_user
        if user.id not in context.bot_data:
            bot.send_message(user['id'], xplay_msg)
            return

        player = context.bot_data[user.id]
        # TODO
        # handle the case where a plyaer could be part of many games
        curent_game = player.game

        if not self.check_bid(bot, user['id'], curent_game, player, cmd[1]):
            return

        group_id = curent_game.chat_id
        if curent_game.is_round_complete():

            bot.send_message(group_id, f"{curent_game.get_bids()}")
            # post round results in the end
            self.post_round(bot, group_id, curent_game)
            curent_game.next_round()

            if curent_game.is_complete():
                self.post_final(bot, group_id, curent_game)

            else:
                self.req_bid(bot, group_id, curent_game)

            self.clean_up(update, context)

    def clean_up(self,  update: Update, context: CallbackContext) -> None:
        """
            Cleans up data releated to a specific game
        """
        pass

    def show_ins(self, update: Update, context: CallbackContext) -> None:
        """
        Prints instruction to the one requesting it
        """
        bot = context.bot
        chat_id = update.message.chat_id

        bot.send_message(chat_id, ins_msg)

    def show_cmd(self, update: Update, context: CallbackContext) -> None:
        """
        Prints instruction to the one requesting it
        """
        bot = context.bot
        chat_id = update.message.chat_id

        bot.send_message(chat_id, cmd_msg)

    def engine(self,  update: Update, context: CallbackContext) -> None:
        """
        This is the function that should ideally be used to call
        engine functions. It will call the respective function according
        to the command"""

        chat_type = update.message.chat.type
        cmd = update.message.text.split(" ")[0]

        if cmd in self.cmd_map:
            if chat_type in self.cmd_map[cmd][0]:
                self.cmd_map[cmd][1](update, context)
