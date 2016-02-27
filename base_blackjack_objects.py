# cfd blackjack base classes

# library imports

from random import shuffle

# deck class

class Deck(object):
    
    def __init__(self, num_decks=4):
        self.new_cards(num_decks)
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
        if self.num_cards_left == 0:
            self.new_cards()
            self.shuffle()
        return self.cards.pop()
        
# create score dictionary to evaluate hand scores

score_dict = {}
for card in xrange(2,11):
    score_dict[str(card)] = card
for card in ['J','Q','K']:
    score_dict[card] = 10
score_dict['A'] = [1,11]

# create set of blackjack hands to check against

blackjack_hands = set()
for c in ['10','J','Q','K']:
    blackjack_hands.add((c,'A'))
    blackjack_hands.add(('A',c))
   
# hand class
         
class Hand(object):     

    def __init__(self, cards=None):
        if cards:
            self.cards = cards
        else:
            self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)
        
    def possible_scores(self):
        
        # first check for blackjack hands
        
        if tuple(self.cards) in blackjack_hands:
            return 'blackjack'

        # if not, work out numeric hand score

        hand_score = [0]
        for card in self.cards:
            card_score = score_dict[card]
            if card == 'A':
                temp = hand_score[:]
                hand_score = []
                for temp_score in temp:
                    hand_score += [x+temp_score for x in card_score]
                new_hand_score = list(set(hand_score))
            else:
                new_hand_score = [x+card_score for x in hand_score]
            hand_score = new_hand_score[:]

        return hand_score
   
    def best_score(self):
        
        # first get possible scores
        
        possible_scores = self.possible_scores()
        
        # check for blackjack
        
        if possible_scores == 'blackjack':
            return 'blackjack'
            
        # otherwise, find maximum score less than or equal to 21
            
        valid_scores = [x for x in possible_scores if x <= 21]
        if valid_scores:
            best_score = max(valid_scores)
        else:
            best_score = 'bust'
        
        return best_score
        