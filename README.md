# Game_91_tg_bot

## Intro

Game 91 is a card game that has a good amount of game theory. The rules are easy, the game is simple but it is exciting and fun. The inspiration for this project came from the love of this game, and the need to do it online as in person implementations have come to halt during the current global situation. This repositroy holds a program for a telegram bot that facilitates this game.

For any one who wants to enjoy the game here is a file describing all the rules. [Here](./rules.md)

If you have read the rules or if you already know them lets see how we went about its telegram implementation.

In a face to face, game everyone would be facilitating and making sure the rules are being folled making sure a succesful game takes place, but in virtual case we will need some one to do that, and that is what this bot is for. In short, what the bot does is it collects bids from every envolved player, and then once everyone is done bidding, it anounces everyonce bid and who the winner was. It then post the next round prizes, and continue with the same logic till the game end. In doing so it also handle ties, wrong inputs and all the things a facilitor of a game would do. Once the game is complete, it announces the winner, and presents a nice gif. The gifs are also presented for every round winners. The bot could be added to a group, or a super group. And as of version 1 it allows multiple games to be played in the same group, and a player could take part in multiple games in multiple groups the will just have to know the ids of each game, which will be given during their creation.

Once the bot is added to the group users can interact with it with the following sets of commands.

```
comands to interact with the bot
****************************
- `.C` or `!CRT` - create command that creates a game session and sends the game id

- `.J <game id>` or `!JOIN <game id>` - adds the player who types the command to the game identified by the game id. The game id can be seen from the create command command response

- `.S <game id>`  or `!STR <game id>` - start command, that tells the bot that all players have been added and hence it should start the game.

- `.B <value> <game id>` or `!BID <value> <game id>` - Command used to bid for a card in private message <value> - is that ammount you want to bid, game id is the id of that game you are playing

- `.I` or `!INS` - gives the instruction of the game and how to play it

- `.M` or `!CMD` - Gives this list of commands and their functinoality

- `.F Feedback` or `!FED  Feedback` -  Sends feedback to the developers, it can be in private, or group chats
     eg: 1. !FED "When I typed !BID it gave the wrong result"
         2. !FED "I really like this game but this this could be improved"
         3. !FED "I don't like the user experience it could be improved by"

- `.ST <game id>` or `!STAT game id` - shows status in the private chat, you can see the cards you won and the cards you have left in the <game id> game with this command if no game id is provided it will show all your status across all the mutliple games you are participating in
```

Some of the commands can only be used either in group chats or private chats and other could be used in both like !INS and !CMD. This commands are planned to be simplifed in version 2 with keyboard input support.

## Structure

The way this repository is organized is as follows.

The main entry point is the [g91_tgbot](./g91_tgbot.py) python file. This will be where all the things like message handlers, updaters and dispathcers are defined and initiated. The main method that handels all the incoming messages is the G91_tgingin().engine method. This merhod as you can see is part of the G91_tgingin class, as grouping the multiple functions this game engine sounds a more convinent way to go about the problem as you may see. All things related to the idea of Game 91 are defined in the [game91](./game91/) directory. This includs the modules defining the G91_tgingin, which is a class full of methods usefull for handling different inputs, the Game_91 class which is a mutli purpose class discreption of all the methods and properties needed by the game. This class is multipurpose and could in the future be used with other engines like in web apps. In this program it is being used for maninpulating games with the game91_ingine.

The card_games and card_players directories as their name indicates holds modules defining player and card objecss that will in cooperation with the game91 class be used by the enigne to run a game

A short nice description of this program would be something along the line of:

=> Python telegram bot module provides methods to interact with the telegram api to collect inputs from users and groups that have allowed the bot, then the Engine takes the input and create Game object or Player object or Go to the next round of the game or send a congratulation message, depending on the input.

Tests - are collection of tests that use the ptbtest liberary
Ptbtest - is a modified version of the outdated ptbtest liberary from [here](https://github.com/Eldinnie/ptbtest)
Data - holds card images that will be send by the bot. DON'T CHANGE THE NAME OF THE IMAGES AS THE BOT DEPENDS ON THAT TO FIND THE CORRECT FILE.

The program has been commented as much as possible, and follows all pep8 rules so it should be easy to navigate having this structure information. If you would like to contribute, use the dev branch. And if you have any questions reach out to me, I would love to answer your questions.

## Author

Hileamlak M. Yitayew
Copyright (C) 2021
