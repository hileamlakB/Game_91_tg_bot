#!/usr/bin/env python3.8
"""
This file containes all the messages used by the
telegram game 91 engine
"""

# if this messages are changed make sure the unittests
# are also changed since the depend on the messages
game_created = """
**********************************
Game Created
Game Id: {}

We now need some players to the start the game.

In this game we at least need {} players, and at most {} players.

Any one who wants to play can type !JOIN <game id> (the game id \
value instead of <game id>). They will then automatically be \
added to the current Game.

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

The game has reached its maximum player Limits. you can start \
another game later.

For now, you can start playing by tying the !STR command
****************************************
"""
noid_msg = """
Specify which game to join using game id.
For more information on how to use different
commands type !inf
"""
xaddp_msg = """
Game has already started!!

Can't add a new player! you can join another game later. Or \
create a new one with the create command.

For more info, on commands type !CMD
"""
xgame_msg = """
No such game id. The game id should be the correct one.

Create a new game if you don't have one.

For more infor about the commands type !CMD
"""
xuser_msg = "For the bot to be able to receive your bid you have \
to initialize a conversation with it. You can do that by going \
to @game_91_bot and pressing start. After that you can retype \
the !STR command"
started_msg = "The game is now started no more players can be added!\
you can now play. Type !INS anytime to see instructions."
fround_msg = """
Round one has begun!!!

Players, make you bids in private chats.
"""
init_msg = "The game is already started. Enjoy it!!"
bid4_msg = "You are now bidding for the {} of {}"
bid_msg = "Make your round {} bids!!"
nstart_msg = "The game isn't ready to be started! Add more players"
win_msg = "Congratulation {}! You won the game with {} points {}"
ins_msg = """
Players and Cards
**************************
The game is for two to seven players, using a complete suit from a standard\
52-card pack for each player plus one extra suit. Two decks are needed for\
four or more players. Cards rank Ace \
(low), 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K (high). As a prize, \
the Ace is worth 1 point, cards 2-10 face value, Jack 11, \
Queen 12 and King 13.

Setup
***************************
The cards are sorted into suits. One suit (traditionally diamonds) is \
turned face down and presented as a prize pile by the bot. \
Each of the other players takes one complete suit.


Play
***************************
A random card from the prize pile is selected by the bot randomly. \
Then each player selects a card from their pile and try to bid \
for the prize on a private chat with the bot. When all players\
finish bidding, the bot anounces what everyone bided and who\
the winner of the round is. The winner get to add the won \
card to their pile of won cards. Then another card  \
will be selected by the bot and players bid for it \
in the same way they run out of their cards. If \
two players put the highest bid, the bid doesn't \
count, but the prize card remains on offer in \
the next round along with the next round's prize.\
The same thing happens if two people or more \
players bid the highest bid in a round \
until some one wins all the acumulated \
prize. If the tie keeps happening \
until the end, the accumulated prize is discarded once \
all the players run out of cards to play with.

Scoring
**************************
When all players run out of bid cards the play ends.\
Each player totals the value of the diamonds they \
have won in bids (ace=1, 2-10 face value, J=11, Q=12, K=13) \
and the greater total wins the game.

Variation (Future version)
**************
Inorder to hanndle ties Another card is turned from the prize \
pile and the players bid again. It needs \
to be agreed whether players not involved \
in the original tie for highest are eligible to \
win in the second round of bidding.

Interacting with the bot
*********************
To play this game, you have to creat a game first \
you can do that by typing the creat command \
which is `!CRT`.

All commands in this bot start  with `!`. \
And you can learn more about them if \
you type `!CMD`.
"""
cmd_msg = """
comands to interact with the bot
****************************
=> `.C` or `!CRT` - create command that creates a game session and sends the game id

=> `.J <game id>` or `!JOIN <game id>` - adds the player who types the command to the game \
identified by the game id. The game id can be seen from the \
the creat command command response

=> `.S <game id>`  or `!STR <game id>` - start command, that tells the bot that all \
players have been added and hence it should start the game.

=> `.B <value> <game id>` or `!BID <value> <game id>` - Command used to bid for a card in private message \
    <value> - is that ammount you want to bid, game id is the id of that game you are playing

=> `.I` or `!INS` - gives the instruction of the game and how to play it

=> `.M` or `!CMD` - Gives this list of commands and their functinoality

=> `.F Feedback` or `!FED  Feedback` -  Sends feedback to the developers, it can be in private, or group chats
     eg: 1. !FED "When I typed !BID it gave the wrong result"
         2. !FED "I really like this game but this this could be improved"
         3. !FED "I don't like the user experience it could be improved by"

=> `.ST <game id>` or `!STAT game id` - shows status in the private chat, you can see the cards you won and the cards you have left in the <game id> game with this command
if no game id is provided it will show all your status across all the mutliple games you are participating in
"""
tie_msg = """
There was a tie in this round no one won this  time.
The prize will go the next round and will be agrigated with the next \
round's prize
"""
xplay_msg = "You aren't playing any game! Go to your favorite group and \
create one"
nbid_msg = "Please specify the bid amount!!"
nid_msg = "Please specify to which game you want to bid with the game id \
you got during the creation!!"
xconb_msg = "You can't bid now! wait till this round is over!"
xcard_msg = "You can't bid with that card you don't have it!"
bids_msg = "Your bid has been recorded!! Go back to {}"
xug_msg = "You are not a part of this game!!"
urc_msg = "Here are your current cards!!\n"
test_msg = """Hello!! I am gald you are playing me!!
In this Private chat you will tell me your bids!! And I will keep them \
a secreat until the time comes!!.
For a start you have the following cards\n
{} for the game {}.

We will start shortly when everyone has initialized a conversation
with me.\n\n
To see the cards you have and the cards you won
you can type the .St <game id> here at any time.

And remeber when you bid a card you loose it, so you won't be able to bid\
with it again"""
bidh_msg = "\nTo bid you can do .B <value> <game_id>"
stat_msg="""
In {}
-------------
Left: {}

Wons: {}

---------------

"""
