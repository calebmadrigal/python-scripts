#!/usr/bin/env python

import sys

SUITS = ['S', 'C', 'H', 'D']
DENOMS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class CardException(Exception):
   pass

class Card:
   def __init__(self, card_string):
      try:
         if len(card_string) == 3:
            self.denom = card_string[0:2].upper()
            self.suit = card_string[2].upper()
         else:
            self.denom = card_string[0].upper()
            self.suit = card_string[1].upper()

         if self.denom not in DENOMS:
            raise CardException("Card has incorrect denom")

         elif self.suit not in SUITS:
            raise CardException("Card has incorrect suit")

      except:
         raise CardException("Failed to parse card")

      print "Card: %s of %s" % (self.denom, self.suit)

class PokerHand:
   def __init__(self, cards):
      self.cards = []
      for c in cards:
         self.cards.append(Card(c))

      # Sort cards according to index in denom
      self.cards.sort(lambda x,y: DENOMS.index(x.denom) - DENOMS.index(y.denom))

   def number_of_suit(self, suit):
      count = 0
      for card in self.cards:
         if card.suit == suit:
            count = count + 1
      return count

   def number_of_denom(self, denom):
      count = 0
      for card in self.cards:
         if card.denom == denom:
            count = count + 1
      return count

   def suit_distribution(self):
      """ Returns a list: [#spades, #clubs, #hearts, #diamonds]. """

      distribution = []
      for suit in SUITS:
         distribution.append(self.number_of_suit(suit))
      return distribution

   def denom_distribution(self):
      """ Returns a list: [#2's, #3's, #4's, etc]. """

      distribution = []
      for den in DENOMS:
         distribution.append(self.number_of_denom(den))
      return distribution

   def hand_name(self):
      if self.is_royal_flush():
         return "Royal flush"
      elif self.is_straight_flush():
         return "Straight flush"
      elif self.is_four_of_a_kind():
         return "Four of a kind"
      elif self.is_flush():
         return "Flush"
      elif self.is_full_house():
         return "Full house"
      elif self.is_straight():
         return "Straight"
      elif self.is_three_of_a_kind():
         return "Three of a kind"
      elif self.is_two_pair():
         return "Two pair"
      elif self.is_one_pair():
         return "One pair"
      else:
         return "High card: %s" % self.cards[-1].denom

   def is_royal_flush(self):
      # Hand is a royal flush if it is a straight flush that contains an Ace.
      return self.is_straight_flush() and self.number_of_denom('A')

   def is_straight_flush(self):
      return self.is_flush() and self.is_straight()

   def is_flush(self):
      return self.suit_distribution().count(5)

   def is_four_of_a_kind(self):
      return self.denom_distribution().count(4)

   def is_three_of_a_kind(self):
      return self.denom_distribution().count(3)

   def is_full_house(self):
      dist = self.denom_distribution()
      return dist.count(2) and dist.count(3)

   def is_two_pair(self):
      dist = self.denom_distribution()
      return dist.count(2) == 2

   def is_one_pair(self):
      dist = self.denom_distribution()
      return dist.count(2)

   def is_straight(self):
      # Since cards are sorted, start with first card and if each subsequent card
      # matches the corresponding subsequent card in DENOMS, it is a straight.
      for i in range(len(self.cards)-1):
         if DENOMS.index(self.cards[i].denom)+1 != DENOMS.index(self.cards[i+1].denom):
            return 0
      return 1

if __name__ == "__main__":
   hand = sys.argv[1:]

   if len(hand) != 5:
      print "Usage: poker_hand.py QH KS 5C 2D JC"
      sys.exit(1)
   else:
      try:
         hand = PokerHand(hand)
         print hand.hand_name()
      except CardException, e:
         print "ERROR: ", e
