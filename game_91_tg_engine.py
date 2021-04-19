#!/usr/bin/env python3.8

import logging
import uuid

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import Unauthorized

from game_91 import Game_91
from player import Player

from telegram_handlers import start, help_command

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few recommended command handlers.


def game_91_engine(update: Update, context: CallbackContext) -> None:
    """Accorind to the message handels different game commands."""
    msg = update.message.text.split(" ")
    chat_id = update.message.chat_id
    bot = context.bot

    if msg[0] == "MC!create" and not context.chat_data:
        game = Game_91()
        game.chat_id = str(chat_id)
        #use game id here 1 is for ease for now
        context.chat_data["1"] = game
        context.bot_data[chat_id] = game
        bot.send_message(chat_id=chat_id,
                         text="""
                             *********** Game 1 Created **************
                             Lets now add players. We need 3. each player should type !player <game_id_they_want_to_join>

                                """)
    elif msg[0] == "MC!player" and int(
            msg[1]) == 1:  #check if the game id is a proper one
        current_game = context.chat_data["1"]
        user = update.effective_user
        player = Player(update.effective_user.first_name, current_game,
                        "SPADE")
        player.user = update.effective_user

        if current_game.add_player(player) == 1:
            context.bot_data[user.id] = player
            if current_game.is_ready():
                bot.send_message(
                    chat_id=chat_id,
                    text=
                    """ The game is now ready to be played, it has enough player!! You can go and play if you play type MC!start"""
                )
    elif msg[0] == "MC!start" and int(msg[1]) == 1:

        current_game = context.chat_data["1"]
        is_init = True

        if current_game.is_started:
            bot.send_message(chat_id,
                             "The game is already started. Keep playing")

        elif current_game.is_ready():
            for player in current_game.get_players():
                try:
                    player_user_id = player.user['id']
                    bot.send_message(
                        chat_id=player_user_id,
                        text=f"""Make your round {current_game.round} bids""")
                except Unauthorized:
                    is_init = False
                    bot.send_message(
                        chat_id,
                        f"For the bot to be able to recieve your bid you have to initalize a conversation with you. You can do that by going to @my_bot and pressing start. Player {player.user['first_name']} hasn't initalized the bot"
                    )
            if is_init:
                current_game.start()
                bot.send_message(
                    chat_id,
                    "The game is now started no more players cant be added! you can know play. type /ins to see instructions"
                )
                bot.send_message(
                    chat_id,
                    "Round one has begun!! Players make you bid in private messages. For the bot to be able to get your messages and start collecting your bids got to @my_bot and press start"
                )
                bot.send_message(
                    chat_id,
                    f"You are now bidding for the {current_game.current_prize[1]} of {current_game.current_prize[0]}"
                )
                for player in current_game.get_players():
                    player_user_id = player.user['id']
                    bot.send_message(
                        chat_id=player_user_id,
                        text=f"""Make your round {current_game.round} bids""")
    elif msg[0] == "MC!bid" and update.message.chat.type == "private":
        user = update.effective_user
        if context.bot_data[user.id]:
            player = context.bot_data[user.id]
            current_game = player.game
            current_game.add_bid(player, int(msg[1]))
            group_id = current_game.chat_id
            if current_game.is_round_complete():
                if current_game.is_complete():
                    bot.send_message(group_id, f"{current_game.get_bids()}")
                    print(current_game.is_complete(),
                          current_game.is_round_complete(), current_game.round)
                    winner = current_game.handle_winner()
                    if winner[0] != None:
                        bot.send_message(group_id,
                                         f"{winner[0].name} won this round")
                    f_winner = current_game.final_winner()
                    if f_winner[0]:
                        bot.send_message(
                            group_id,
                            f"Congratulation {f_winner[0].name}! You won the game with {f_winner[1]} points"
                        )

                else:
                    bot.send_message(group_id, f"{current_game.get_bids()}")
                    winner = current_game.handle_winner()
                    if winner[0] != None:
                        bot.send_message(group_id,
                                         f"{winner[0].name} won this round")
                        current_game.next_round()
                        bot.send_message(
                            group_id,
                            f"You are now bidding for the {current_game.current_prize[1]} of {current_game.current_prize[0]}"
                        )
                        for player in current_game.get_players():
                            player_user_id = player.user['id']
                            bot.send_message(
                                chat_id=player_user_id,
                                text=
                                f"""Make your round {current_game.round} bids"""
                            )

        else:
            bot.send_message(
                user['id'],
                "You aren't playing any game! Go to a group and create one")

def main() -> None:

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1762593952:AAE2tYivmziMiu8jn0aJrDW1ENbQY_JM9qs",
                      use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, game_91_engine))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
