#!/usr/bin/env python3.8
"""
This file containes all the messages used by the
telegram game 91 engine
"""

game_create =  """
**********************************
* Game {} created                *
* We now need players to play    *
* the start the game.            *
*                                *
* In this game we at least need  *
* {} players, and at most {}     *
* players.                       *
*                                *
* Any one who wants to play can  *
* type !ADD {game_id}. They will *
* then automatically be added to *
* the current Game.              *
*                                *
* Waiting for you to join!!      *
**********************************
"""
ready_msg = """
****************************************
* The game is now ready to be played!!!*
* it has enough player!! You can also  *
* add some more.                       *
*                                      *
* You can go and play by inserting the *
* !STR command                         *
****************************************
"""
maxp_msg = """
****************************************
* Couldn't Add player! The maximum.    *
* The game has reached its player      *
* Limits. you can start another game   *
* later.                               *
*                                      *
* For now, you can start playing by    *
* tying the !STR command               *
****************************************
"""
noid_msg = """
Specify which game to join using game id.
For more information on how to use different
commands type !inf
"""
xaddp_msg="""
Game has already started!! Can't add
a new player! you can join another game
later. Or create a new one with the create
command. For more info, on commands type
!inf
"""
xgame_msg="""
No such game id. The game
id should be the correct one.
Create a new game if you don't have one.
For more infor about the commands type !inf
"""
xuser_msg = """
For the bot to be able to receive your bid
you have to initalize a conversation with it.
You can do that by going to @my_bot and
pressing start."""
init_msg = """
The game is already started. Enjoy it!!
"""
started_msg="""
The game is now started no more players can
be added! you can know play. Type !INS any
time to see instructions
"""
fround_msg="""
Round one has begun!!
Players, make you bids in private chats.
"""
bid4_msg="You are now bidding for the {} of {}"
bid_msg="Make your round {} bids"
nstart_msg = "The game isn't ready to be started! Add more players"