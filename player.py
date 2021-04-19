#!/usr/bin/env python3.8
"""
Defines a card game player object
"""


class Player:
    """ A player for card games """

    def __init__(self,
                 name: str,
                 game,
                 card_suit: str,
                 card_amount="ALL"):
        """ Creates a card player object.
        The player is suited to be a card game 
        player

        Attributes
        @name - name of the player could also be used
                a specific identifier
        @game - the game to which this player belong to
        @cards - the cards this player own
        @won - the cards won by this player
        @bids - the bids made by this player in the current round
        @can_bid - status of the players ability to bid on a round
                   used to make sure that a player wont bid more than
                   once
        @total_points - The total point won calculated using the won cards
        """

        self.name = name
        self.game = game
        self.cards = Cards(**{card_suit: card_amount})
        self.cards.set_suit(card_suit)
        self.won = []
        self.bids = []
        self.can_bid = True
        self.total_points = 0

    def add_bid(self, bid, suit=None):
        """ 
        Adds the current bid of this player at the end of the bid list
        and changes the bidding status of the player.

        Takes the bid amount and the suit, which by default is set to
        the suit of the house

        Returns the bid card on success
        or an empty list if it fails
        """

        if not suit:
            suit = self.cards.suit

        if self.can_bid:
            removed = self.cards.remove([suit, bid])
            if removed:
                self.bids.append(removed)
                self.can_bid = False
                return removed
            return []
        return []

    def add_won(self, suit, value):
        """
        Adds a card to the players won list
        """
        self.won.append([suit, value])

    def calculate_total(self):
        """
        Calculates the total won points using
        the self.won list

        Returns the total point of the cards won
        """

        self.total_points = 0
        for card in self.won:
            self.total_points += int(card[1])

        return self.total_points
