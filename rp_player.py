# basic player classes

# prototype player class

import sys

class RPPlayer(object):

    def __init__(self, name='RP'):
        self.amount_actually_bet = 0
        self.minimum_kitty = 70
        self.increase_bet_threshold = 9
        self.increase_bet_max_mult = 2
        self.name = name
        self.count = 6
        self.cards_in_shoe = 52*4
        self.cards_played = 0

    def bet(self, current_funds, minimum_bet, maximum_bet):
        return minimum_bet

    def betx(self, current_funds, minimum_bet, maximum_bet):
        mult = self.increase_bet_max_mult if self.count >= self.increase_bet_threshold else 1.0
        return minimum_bet*mult

    def bet_count_full(self, current_funds, minimum_bet, maximum_bet):
        mult = self.count - self.increase_bet_threshold + 2
        if mult <= 0:
            mult = 1.0
        elif mult > self.increase_bet_max_mult:
            mult = self.increase_bet_max_mult
        proposed_bet = min(minimum_bet*mult,maximum_bet)
        self.amount_actually_bet = minimum_bet if current_funds - proposed_bet < self.minimum_kitty else proposed_bet
        self.current_funds = current_funds
        return self.amount_actually_bet

    def play(self, current_hand, current_table):
        # use dealer rules
        possible_scores = current_hand.possible_scores()

        if possible_scores == 'blackjack':
            return 'stand'

        # check for must-stand scores

        for score in possible_scores:
            if score >= 17 and score <= 21:
                return 'stand'

        dealer_visible_card = current_table['Dealer'][0]
        if (dealer_visible_card == '2' or dealer_visible_card == '3' or \
        dealer_visible_card == '4' or dealer_visible_card == '5' or dealer_visible_card == '6') \
        and max(possible_scores) > 12:
            # dealer has weak hand
            return 'stand'
        else:
            return 'hit'

    def final_look(self, final_table):
        cards_left_before = self.cards_in_shoe - self.cards_played
        for hand in final_table.values():
            opp = len([str(j) for j in hand if j.isdigit() and int(j) < 7]) - 1
            for card in hand:
                self.cards_played += 1
                if self.cards_played >= self.cards_in_shoe:
                    self.count = 6
                    self.cards_played = 0
        self.count += opp
#        print "Cash: %d, Bet: $%d  Count: %d, Hand: %s" % (self.current_funds, self.amount_actually_bet, self.count, final_table['Robert'])
