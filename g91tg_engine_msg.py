#!/usr/bin/env python3.8
"""
This file containes all the messages used by the
telegram game 91 engine
"""

game_created =  """
**********************************
 Game Created
 Game Id: {}

 We now need some players to the start the game.

 In this game we at least need {} players, and at most {} players.

 Any one who wants to play can type !ADD <game id> (the game id value inside <>). They will then automatically be added to the current Game.

 Waiting for you to join!!
**********************************
"""
ready_msg = """
****************************************
 The game is now ready to be played!!!
 It has enough player!! You can also add some more.

 You can go and play by inserting the !STR command
****************************************
"""
maxp_msg = """
****************************************
 Couldn't add new player!

 The game has reached its maximum player Limits. you can start another game later.

 For now, you can start playing by tying the !STR command
****************************************
"""
noid_msg = """
Specify which game to join using game id.
For more information on how to use different
commands type !inf
"""
xaddp_msg="""
Game has already started!!

Can't add a new player! you can join another game later. Or create a new one with the create command.

For more info, on commands type !CMD
"""
xgame_msg="""
No such game id. The game id should be the correct one.

Create a new game if you don't have one.

For more infor about the commands type !CMD
"""
xuser_msg = """
For the bot to be able to receive your bid you have to initalize a conversation with it. You can do that by going to @game_91_bot and
pressing start."""
started_msg="""
The game is now started no more players can be added! you can now play. Type !INS any
time to see instructions.
"""
fround_msg="""
Round one has begun!!!

Players, make you bids in private chats.
"""

init_msg = "The game is already started. Enjoy it!!"
bid4_msg="You are now bidding for the {} of {}"
bid_msg="Make your round {} bids"
nstart_msg = "The game isn't ready to be started! Add more players"

ins_msg="""
Players and Cards
**************************
The game is for two to seven players, using a complete suit from a standard 52-card pack for each player plus one extra suit. Two decks are needed for four or more players. Cards rank Ace (low), 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K (high). As a prize, the Ace is worth 1 point, cards 2-10 face value, Jack 11, Queen 12 and King 13.

Setup
***************************
The cards are sorted into suits. One suit (traditionally diamonds) is turned face down and presented as a prize pile by the bot. Each of the other players takes one complete suit.


Play
***************************
A random card from the prize pile is selected by the bot randomly. Then each player selects a card from their pile and try to bid for the prize on a private chat with the bot. When all players finish bidding, the bot anounces what everyone bided and who the winner of the round is. The winner get to add the won card to their pile of won cards. Then another card  will be selected by the bot and players bid for it in the same way they run out of their cards. If two players put the highest bid, the bid doesn't count, but the prize card remains on offer in the next round along with the next round's prize. The same thing happens if two people or more players bid the highest bid in a round until some one wins all the acumulated prize. If the tie keeps happening until the end, the accumulated prize is discarded once all the players run out of cards to play with.

Scoring
**************************
When all players run out of bid cards the play ends. Each player totals the value of the diamonds they have won in bids (ace=1, 2-10 face value, J=11, Q=12, K=13) and the greater total wins the game.

Variation (Future version)
**************
Inorder to hanndle ties Another card is turned from the prize pile and the players bid again. It needs
to be agreed whether players not involved in the original tie for highest are eligible to win
in the second round of bidding.

Interacting with the bot
*********************
To play this game, you have to creat a game first youcan do that by typing the creat command which is `!CRT`.

All commands in this bot start  with `!`. And you can learn more about them if you type `!CMD`.
"""
cmd_msg="""
cmds to interact with the bot
****************************
=> `!CRT` - create command that creates a game session and sends the game id

=> `!ADD <game id>` - adds the player who types the command to the game session identified by the game id. The game id can be seen from the the CRT command response

=> `!STR <game id>` - start command, that tells the bot that all players have been added and hence it should start the game.

=> `!BID <game id>` - Command used to bid for a card in private message

=> `!INS` - gives the instruction of the game and how to play it

=> `!CMD` - Gives this list of commands and their functinoality
"""