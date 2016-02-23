# cfd blackjack initial test

# library imports

from random import shuffle

# deck class

class Deck(object) :
    
    def __init__(self, num_decks=4):
        self.newcards(num_decks)
        self.shuffle()

    def newcards(self, num_decks=4):
        self.cards = []
        for c in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
            for d in xrange(4*num_decks):
                self.cards.append(c)
        self.num_cards_left = len(self.cards)
    
    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        self.num_cards_left -= 1
        return self.cards.pop()
            
    


