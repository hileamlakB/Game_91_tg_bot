#!/usr/bin/env python3.8
"""
Defines game objects
Mostly the games are card games
that are ideal for math camps
"""
import uuid
from cards import Cards
from player import Player
from cardgame import CardGame


class Game_91(CardGame):
    """ 
    A game object for the 91 card game 
    rules for the game can be found in 
    the pdf file in this repository.

    Attributes
    @MAX_PLAYERS - the maximum number of players
                 that could take part in the game
    @MIN_PLAYERS - the minimum number of players
                 that could take part in the game
    """

    MAX_PLAYERS = 3
    MIN_PLAYERS = 2

    def __init__(self):
        """
        Creates a game 91 object, which can be 
        used to store and manipulate different
        datas about players and score in different
        stages of the game. It works well with a game
        engine.

        Attributes
        @id - a unique identifier of the game object
              to allow initiation of multiple game objects
        @players - the list of player taking part in this game
        @game_stat - ?
        @is_started - the status of the game
        @round - a number showing the current round
        @prize_cards - a list of cards that are to be presented
                     as a prize
        @current_prize - a new prize withdrawen from the prize_cards
                      after every round. in case of tie there could
                      be more than one in the round next to the tie
                      other wise it is similar to the current prize
        @bids - is the list of bids made and also the details  about
              the bid including the bidder in a key-value pair
        """
        self.id = str(uuid.uuid4())
        self.players = []
        self.game_stat = False
        self.is_started = False
        self.round = None
        self.prize_cards = None
        self.current_prize = None
        self.bids = {}

    def add_player(self, player: Player):
        """
        Addes a new player to
        the current game if it isn't full
       
        Returns True on success and False on failer
        This will only fail if the maximum number of
        players is reached
        """

        if len(self.players) < Game_91.MAX_PLAYERS:
            self.players.append(player)
            return True
        return False

    def show_status(self):
        """ 
        Returns a string containing
        the status of each player and
        the whole game separated by a
        new line
        """

        stat = ""
        for player in self.players:
            stat += str(player) + "\n"
        stat += self.game_stat

    def get_players(self):
        """Getter for the list of players"""
        return self.players

    def is_ready(self):
        """
        Checks if the game is ready to be started
        according to the rules
        
        Returns True if it is and False if not
        """

        if len(self.players) in range(Game_91.MIN_PLAYERS,
                                      Game_91.MAX_PLAYERS):
            return True
        return False

    def start(self):
        """
        Changes the status of the game as started,
        Sets the round, the prize_cards and other variables
        
        If the game is already started it does nothing.
        Returns  None in both cases
        """

        if not self.is_started:
            self.is_started = True
            self.round = 1
            self.prize_cards = Cards(CLUB="ALL")
            self.current_prize = self.prize_cards.get_random()
            self.prize_cards.set_suit("CLUBS")

    def add_bid(self, player: Player, bid: int):
        """
        Records bid made in the bids dictionary.
        The round will be the key and the value will
        be a dictionary having the player as a key and the
        bid amount as a value. It first checks if the player
        hasn't already bided by first adding the bid to the 
        player object.

        Returns the result of adding the bid to the player object
        """

        p_bid = player.add_bid(bid)
        if p_bid:
            if f"{self.round}" in self.bids:
                self.bids[f"{self.round}"].append({player: bid})
            else:
                self.bids[f"{self.round}"] = [{player: bid}]
        return p_bid

    def is_round_complete(self):
        """ 
        Checks if the current round is complete
        by counting the number of bids made

        Returns True if it is and False if it isn't
        """
        if len(self.bids[f"{self.round}"]) == len(self.players):
            return True
        else:
            return False

    def next_round(self):
        """
        Moves the game into the next round if the 
        current round is complete. And give back all
        the players their ability to bid again.

        Returns True if the bid was successful and
        False if it isn't.
        """

        if self.is_round_complete():
            self.round += 1
            for player in self.players:
                player.can_bid = True
            #self.current_prize = self.prize_cards.get_random()
            return True
        return False

    def is_complete(self):
        """
        Checks if the game is complete by checking
        the number of  prize cards left.
        """

        if self.prize_cards.ncards() == 0:
            return True
        return False

    def get_bids(self):
        """
        Returns the bids made in the current round

        The format of the returned string is as follows
        "
          {player1_name} bid {bid_value}
          {player2_name} bid {bid_value}
        "
        """
        bid_str = ""
        for bid in self.bids[f"{self.round}"]:
            for player, value in bid.items():
                bid_str += f"{player.name} bid {value}\n"
        return bid_str

    def handle_winner(self):
        """
        Handles winners in a round. Only if the round is complete.
        Better to check if the current round is complete before
        calling this function as the retunrned value may create 
        confusion for the caller.
        """
 
        # format [Bidder, bid]
        max_bid = [None, 0]

        if not self.is_round_complete():
            return max_bid

        # choose the maximum bid of this round
        for bid in self.bids[f"{self.round}"]:
            for player, value in bid.items():
                if value > max_bid[1]:
                    max_bid = [player, value]

        # check if there is tie by counting the number of
        # maximum bids
        all_bids = []
        for bid in self.bids[f"{self.round}"]:
            all_bids += [value for _, value in bid.items()]
        if all_bids.count(max_bid[1]) != 1:  #check if there is a repeated maximum
            max_bid = [None, 0]

        if max_bid[0]:
            max_bid[0].add_won(self.prize_cards.suit, max_bid[1])
            if self.prize_cards.ncards() != 0:
                self.current_prize = self.prize_cards.get_random()

        return max_bid

    def final_winner(self):
        """
            Returns the winner by comparing every players won cards
        """
        winner = [None, 0]
        if self.is_complete():
            for player in self.players:
                total = player.calculate_total()
                if total > winner[1]:
                    winner = [player, total]
        return winner
