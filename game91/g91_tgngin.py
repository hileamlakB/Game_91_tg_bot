#!/usr/bin/env python3.8
"""
This file defines a telegram game engine for
the game 91 card game
"""

from telegram import Update
from telegram.ext import  CallbackContext
from telegram.error import Unauthorized

from .g91 import Game_91
from card_players.player import Player
from .g91_msgs import *


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
        "!CRT" : [["group"], self.create_game],
        "!ADD" : [["group"], self.add_player],
        "!STR" : [["group"], self.start_game],
        "!BID" : [["private"], self.bid_card],
        "!INS" : [["group","private"], self.show_ins],
        "!CMD" : [["group","private"], self.show_cmd],
        }

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
        # check if the game id is n the group data
        if game_id not in context.chat_data:
            bot.send_message(chat_id, xgame_msg)
            return

        current_game = context.chat_data[game_id]
        user = update.effective_user
        player = Player(user.first_name, current_game, "SPADE")
        player.user = user

        if user.id in context.bot_data:
            bot.send_message(chat_id, f"{user.first_name} is already added!")
            return

        if current_game.is_started:
            bot.send_message(chat_id, xaddp_msg)
            return

        if not current_game.add_player(player):
            bot.send_message(chat_id, maxp_msg)
            return

        context.bot_data[user.id] = player
        if current_game.is_ready():
            bot.send_message(chat_id, ready_msg)

    def start_game(self, update: Update, context: CallbackContext) -> None:
        """ Starts a game with a specified id """

        cmd = update.message.text.split(" ")

        chat_id = update.message.chat_id
        bot = context.bot
        uusers = []

        if len(cmd) < 2:
            bot.send_message(chat_id, noid_msg)
            return

        game_id = cmd[1]
        if game_id not in context.chat_data:
             bot.send_message(chat_id, nstart_msg)
             return

        current_game = context.chat_data[game_id]
        is_init = True

        if current_game.is_started:
            bot.send_message(chat_id, init_msg)
            return

        if current_game.is_ready():
            for player in current_game.get_players():
                try:
                    pid = player.user['id']
                    bot.send_message(pid, "TEST")

                except Unauthorized:
                    is_init = False
                    uusers.append(player.user['first_name'])

            if is_init:
                current_game.start()
                bot.send_message(chat_id, started_msg)
                bot.send_message(chat_id, fround_msg)
                bot.send_message(chat_id, current_game.get_prize())

                for player in current_game.get_players():
                    pid = player.user['id']
                    bot.send_message(pid, bid_msg.format(current_game.round))
            else:
                msg = xuser_msg + "\n"
                for user in uusers:
                    msg += f"Player {user} hasn't initialized the bot\n"
                bot.send_message(chat_id, msg)



    def bid_card(self, update: Update, context: CallbackContext) -> None:
        """ Allows For cards to be bid in private chats """

        bot = context.bot
        cmd = update.message.text.split(" ")

        user = update.effective_user
        if user.id not in context.bot_data:
            bot.send_message(user['id'], xplay_msg)
            return

        player = context.bot_data[user.id]
        # handle the case where a plyaer could be part of many games
        current_game = player.game

        try:
            bid_stat = current_game.add_bid(player, int(cmd[1]))
        except ValueError:
            bot.send_message(user['id'], "Use a proper card value")
            return

        if bid_stat == None:
            bot.send_message(user['id'], "You can't bid now! wait till this round is over")
            return

        if bid_stat == []:
            bot.send_message(user['id'], "You can't bid with that card you don't have it")
            return

        group_id = current_game.chat_id

        if current_game.is_round_complete():
            if current_game.is_complete():
                bot.send_message(group_id, f"{current_game.get_bids()}")
                winner = current_game.handle_winner()
                if winner[0] != None:
                    bot.send_message(group_id, f"{winner[0].name} won this round")
                else:
                    bot.send_message(group_id, tie_msg)
                f_winner = current_game.final_winner()
                if len(f_winner) == 1:
                    bot.send_message(group_id, win_msg.format(f_winner[0].name, f_winner[1]))
                    self.clean_up(update, context)
                else:
                    w_msg = "No one won!! There was a tie between "
                    for winner in f_winner:
                        w_msg += f"{winner.name}, "
                    bot.send_message(group_id, w_msg)
                    self.clean_up(update, context)

            else:
                bot.send_message(group_id, f"{current_game.get_bids()}")
                winner = current_game.handle_winner()
                if winner[0] != None:
                    bot.send_message(group_id, f"{winner[0].name} won this round")
                else:
                    bot.send_message(group_id, tie_msg)
                current_game.next_round()
                bot.send_message(group_id, current_game.get_prize())
                bot.send_message(group_id, f"Make your round {current_game.round} bids")
                for player in current_game.get_players():
                    pid = player.user['id']
                    bot.send_message(pid, f"Make your round {current_game.round} bids")
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

        cmd = update.message.text.split(" ")[0]
        chat_type = update.message.chat.type

        if cmd in self.cmd_map:
            if chat_type in self.cmd_map[cmd][0]:
                self.cmd_map[cmd][1](update, context)