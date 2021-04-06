#!/usr/bin/env python3.8
import uuid
import random


class CardGame:
    pass


class Cards:
    """ A class to manipulate playing cards """

    #CARD_VALUES = list(range(2, 11)) + ['A', 'J', 'Q', 'K']
    CARD_VALUES = list(range(1, 3))

    def __init__(self, *args, **kwargs):
        """intializes a cards object

        Explain what ALL means and everything
        """
        self.cards = []
        self.suit = ""

        for suit, value in kwargs.items():
            if value == "ALL":
                self.cards += [[suit, x] for x in Cards.CARD_VALUES]
            else:
                self.cards += value

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return card
        return []

    def set_suit(self, suit):
        """Only use if all the cards have similar suit"""
        self.suit = suit

    def get_random(self):
        rand_card = random.choice(self.cards)
        self.cards.remove(rand_card)
        return rand_card

    def length(self):
        return len(self.cards)


class Player:
    """ A player for card games """
    def __init__(self,
                 name: str,
                 game: CardGame,
                 card_suit: str,
                 card_amount="ALL"):
        """ Creates a card player object """
        self.name = name
        self.game = game
        self.cards = Cards(**{card_suit: card_amount})
        self.cards.set_suit(card_suit)
        self.won = []
        self.bids = []
        self.can_bid = True
        self.total_points = 0

    def add_bid(self, bid):
        if self.can_bid:
            removed = self.cards.remove([self.cards.suit, bid])
            if removed:
                self.bids.append(removed)
                self.can_bid = False
                return removed
            return []
        return []

    def add_won(self, value, suit):
        self.won.append([suit, value])

    def calculate_total(self):
        self.total_points = 0
        for card in self.won:
            self.total_points += card[1]
        return self.total_points


class Game_91(CardGame):
    """ A game object for the 91 card game """

    MAX_PLAYERS = 3
    MIN_PLAYERS = 2

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.players = []
        self.game_stat = False
        self.is_started = False
        self.round = None
        self.prize_cards = None
        self.current_prize = None
        self.bids = {}

    def add_player(self, player: Player):
        """ Addes a new player to
        the current game if it isn't full

        also comment about the return types
        """

        if len(self.players) < Game_91.MAX_PLAYERS:
            self.players.append(player)
            return True
        return False

    def show_status(self):
        """ returns a string containing
        the status of each player and
        the whole game separated byt a
        new line"""

        stat = ""
        for player in self.players:
            stat += str(player) + "\n"
        stat += self.game_stat

    def get_players(self):
        """Getter for the player"""
        return self.players

    def is_ready(self):
        """ """
        if len(self.players) in range(Game_91.MIN_PLAYERS,
                                      Game_91.MAX_PLAYERS):
            return True
        return False

    def start(self):
        """ set the is status of the game to started """
        self.is_started = True
        self.round = 1
        self.prize_cards = Cards(CLUBS="ALL")
        self.current_prize = self.prize_cards.get_random()

    def add_bid(self, player: Player, bid: int):
        p_bid = player.add_bid(bid)
        if p_bid:
            if f"{self.round}" in self.bids:
                self.bids[f"{self.round}"].append({player: bid})
            else:
                self.bids[f"{self.round}"] = [{player: bid}]
        return p_bid

    def is_round_complete(self):
        if len(self.bids[f"{self.round}"]) == len(self.players):
            return True
        else:
            return False

    def next_round(self):
        print(self.round, self.round + 1)
        if self.is_round_complete():
            if not self.is_complete():
                self.round += 1
                for player in self.players:
                    player.can_bid = True
                #self.current_prize = self.prize_cards.get_random()

    def is_complete(self):
        if self.prize_cards.length() == 0:
            return True
        return False

    def get_bids(self):
        bid_str = ""
        for bid in self.bids[f"{self.round}"]:
            for player, value in bid.items():
                bid_str += f"{player.name} bid {value}\n"
        return bid_str

    def handle_winner(self):
        max_bid = [None, 0]

        for bid in self.bids[f"{self.round}"]:
            for player, value in bid.items():
                if value > max_bid[1]:
                    max_bid = [player, value]

        #check for tie
        if max_bid[0]:
            all_bids = []
            for bid in self.bids[f"{self.round}"]:
                all_bids += [value for _, value in bid.items()]
            if all_bids.count(max_bid[1]) != 1:  #check if there is a tie
                max_bid = [None, 0]

        if max_bid[0]:
            max_bid[0].add_won(self.prize_cards.suit, max_bid[1])
            if self.prize_cards.length != 0:
                self.current_prize = self.prize_cards.get_random()

        return max_bid

    def final_winner(self):
        winner = [None, 0]
        if self.is_complete():
            for player in self.players:
                total = player.calculate_total()
                if total > winner[1]:
                    winner[player, total]
        return winner