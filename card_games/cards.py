#!/usr/bin/env python3.8
"""
   Defines a Cards class which will be used
   as a container to hold different card instances
   represented as a list of length two containing
   the vale and the suit
"""
import random
import sys


class Cards:
    """ A class to manipulate playing cards """


    CARD_VALUES = list(range(2, 11)) + ['A', 'J', 'Q', 'K']
    SUIT_OPTIONS = ["CLUB", "DIAMOND", "SPADE", "FLOWER"]

    def __init__(self, *args, **kwargs):
        """intializes a cards object

        Takes keyword arguments and returns
        a list of the cards.

        The key could be the suit of the card if any
        keyword argument is passed and the value should
        be a list of tuples discribing the suit and value of a card.
        It could also be `ALL` which means all the the values
        for that suit.
        example:
              * Cards(CLUB=ALL)
              * Cards(CLUB=['A',2,3,4])

        It could also accept a list of cards as part of the args.
        Example:
             * Cards(["CLUB", 4], ["DIAMOND", 7])
        """

        self.cards = [] # set would have been better if lists where hasable
        self.suit = ""

        for suit, value in kwargs.items():
            if suit in Cards.SUIT_OPTIONS:
                if value == "ALL":
                    self.cards += [[suit, x] for x in Cards.CARD_VALUES]
                elif type(value) in [list, str]:
                    self.cards +=[[suit, x] for x in value if Cards.isCard([suit, x])]


        for card in args:
            if Cards.isCard(card):
                if card not in self.cards:
                    self.cards += [card]

    def remove(self, card):
        """
        Removes a card from the set of cards
        Returns
           @the list describing the card if successful
           @empty_list if it fails
        """

        if Cards.isCard(card):
            if card in self.cards:
                self.cards.remove(card)
                return card
        return []

    def set_suit(self, suit):
        """
        This method is idea if all the
        cards have the same suit. And it
        is used to set it.
        Only use if all the cards have similar suit
        """

        self.suit = suit

    def get_random(self, delete=True):
        """
        returns a random card from the list and
        delets it after that unless other wise
        not told not to delete through the delete
        argument
        """

        if len(self.cards) != 0:
            rand_card = random.choice(self.cards)
            if delete:
                self.cards.remove(rand_card)
        else:
            rand_card = [None, None]
        return rand_card

    def ncards(self):
        """
        Returns the number of cards in the list
        """
        return len(self.cards)

    def isin(self, card):
        """
        Checks if card is inside  this card list
        """

        return card in self.cards

    def isCard(card):
        """
        checks if card is in a proper card format
        and returns true if it is. Or False if it isn't
        """

        if len(card) == 2:
            if card[0] in Cards.SUIT_OPTIONS and card[1] in Cards.CARD_VALUES:
                return True
        return False
