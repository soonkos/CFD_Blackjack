# cfd blackjack base classes

# library imports

from random import shuffle
import blackjack_base_players as bj_player

# deck class

class Deck(object):

    def __init__(self, num_decks=4):
        self.new_cards(num_decks)
        self.shuffle()

    def new_cards(self, num_decks=4):
        self.cards = []
        for card in ['2', '3', '4', '5', '6', '7', '8', \
                     '9', '10', 'J', 'Q', 'K', 'A']:
            for card_num in xrange(4*num_decks):
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

SCORE_DICT = {}
for card in xrange(2, 11):
    SCORE_DICT[str(card)] = card
for card in ['J', 'Q', 'K']:
    SCORE_DICT[card] = 10
SCORE_DICT['A'] = [1, 11]

# create set of blackjack hands to check against

BLACKJACK_HANDS = set()
for c in ['10', 'J', 'Q', 'K']:
    BLACKJACK_HANDS.add((c, 'A'))
    BLACKJACK_HANDS.add(('A', c))

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

        if tuple(self.cards) in BLACKJACK_HANDS:
            return 'blackjack'

        # if not, work out numeric hand score

        hand_score = [0]
        for card in self.cards:
            card_score = SCORE_DICT[card]
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

class Game(object):

    def __init__(self, player_list, \
                 table_minimum, table_maximum, starting_funds):
        self.player_list = player_list
        self.table_min = table_minimum
        self.table_max = table_maximum
        self.start_funds = starting_funds

        # other attributes that will be defined later

        self.player_hands = dict()
        self.player_bets = dict()
        self.table = dict()
        self.dealer_card = ''
        self.dealer_hidden_card = ''
        self.dealer_hand = None

        # get the starting deck

        self.deck = Deck()

        # create the dealer player

        self.dealer_player = bj_player.DealerRulesPlayer()

        # give each player some initial cash

        self.player_funds = dict()
        for player in player_list:
            self.player_funds[player.name] = self.start_funds

    def ask_for_bets(self):

        for player in self.player_list:
            current_funds = self.player_funds[player.name]
            bet = player.bet(current_funds, self.table_min, self.table_max)
            self.player_bets[player.name] = bet

    def deal_starting_cards(self):

        # create hand dictionary

        for player in self.player_list:
            self.player_hands[player.name] = Hand()

        # deal out cards

        for card_num in xrange(2):
            for hand in self.player_hands.itervalues():
                hand.add_card(self.deck.deal())
            if card_num == 1:
                self.dealer_card = self.deck.deal()
            else:
                self.dealer_hidden_card = self.deck.deal()

        # create table dictionary showing all cards

        self.table['Dealer'] = (self.dealer_card,)
        for player in self.player_list:
            hand = self.player_hands[player.name]
            self.table[player.name] = tuple(hand.cards)

    def play_hand(self, player):

        # have player play out their hand

        name = player.name
        hand = self.player_hands[name]
        scores = hand.possible_scores()
        play = ''
        while scores != 'blackjack' \
              and any(x <= 21 for x in scores) \
              and play != 'stand':
            play = player.play(hand, self.table)
            if play == 'hit':
                hand.add_card(self.deck.deal())
            scores = hand.possible_scores()

        # update table

        self.table[player.name] = tuple(hand.cards)

    def dealer_play_hand(self):

        # create dealer hand

        self.dealer_hand = Hand([self.dealer_card, self.dealer_hidden_card])

        # play out hand

        scores = self.dealer_hand.possible_scores()
        play = ''
        while scores != 'blackjack' \
              and any(x <= 21 for x in scores) \
              and play != 'stand':
            play = self.dealer_player.play(self.dealer_hand, self.table)
            if play == 'hit':
                self.dealer_hand.add_card(self.deck.deal())
            scores = self.dealer_hand.possible_scores()

        # update table

        self.table['Dealer'] = tuple(self.dealer_hand.cards)

    def settle_bets(self):

        # figure out if players won or lost

        dealer_score = self.dealer_hand.best_score()
        for player in self.player_list:
            name = player.name
            hand = self.player_hands[name]
            score = hand.best_score()
            bet = self.player_bets[name]
            if score == 'blackjack':
                self.player_funds[name] += 1.5*bet
            elif score == 'bust':
                self.player_funds[name] -= bet
            else:
                if dealer_score == 'blackjack':
                    self.player_funds[name] -= bet
                elif dealer_score == 'bust':
                    self.player_funds[name] += bet
                else:
                    if score > dealer_score:
                        self.player_funds[name] += bet
                    elif score < dealer_score:
                        self.player_funds[name] -= bet
                    else:
                        pass

    def final_look_at_table(self):

        for player in self.player_list:
            player.final_look(self.table)





