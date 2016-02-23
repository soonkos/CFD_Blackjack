# cfd blackjack base classes

# library imports

from random import shuffle

# deck class

class Deck(object):
    
    def __init__(self, num_decks=4):
        self.newcards(num_decks)
        self.shuffle()

    def new_cards(self, num_decks=4):
        self.cards = []
        for card in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
            for d in xrange(4*num_decks):
                self.cards.append(card)
        self.num_cards_left = len(self.cards)
    
    def shuffle(self):
        shuffle(self.cards)

    def deal(self):
        self.num_cards_left -= 1
        return self.cards.pop()
        
# create score dictionary to evaluate hand scores

score_dict = {}
for card in xrange(2,11):
    score_dict[str(card)] = card
for card in ['J','Q','K']:
    score_dict[card] = 10
score_dict['A'] = [1,11]
   
# hand class
         
class Hand(object):     

    def __init__(self, cards=[]):
        self.cards = cards
        
    def add_card(self, card):
        self.cards.append(card)
        
    def score(self):
        hand_score = 0
        for card in self.cards:
            card_score = score_dict[card]
            if card == 'A':
                try:
                    hand_score = [x+hand_score for x in card_score]
                except (TypeError):
                    temp = hand_score
                    hand_score = []
                    for temp_score in temp:
                        hand_score += [x+temp_score for x in card_score]
                    hand_score = list(set(hand_score))
            else:
                try:
                    hand_score += card_score
                except (TypeError):
                    temp = hand_score
                    hand_score = []
                    for temp_score in temp:
                        hand_score.append(card_score+temp_score)
                        list(set(hand_score))
        return hand_score
