# try to create a basic blackjack game

import base_blackjack_objects as bj
import base_player_objects as bj_player

# create deck

deck = bj.Deck()

# create the dealer

dealer_player = bj_player.DealerRulesPlayer()

# create the players

player1 = bj_player.ProtoPlayer(name='Steve')
player2 = bj_player.ProtoPlayer(name='Bob')
player3 = bj_player.DealerRulesPlayer(name='Jenny')
player_list = [player1, player2, player3]

# set table minimums and maximums

table_minimum = 5.0
table_maximum = 100.0

# give each player some initial cash

player_funds = dict()
for player in player_list:
    player_funds[player.name] = 100.0

# ask for bets

player_bets = dict()
for player in player_list:
    player_bets[player.name] = player.bet(table_minimum, table_maximum)

# create hand dictionary

player_hands = dict()
for player in player_list:
    player_hands[player.name] = bj.Hand()

# deal out cards

for cnum in xrange(2):
    for name, hand in player_hands.iteritems():
        hand.add_card(deck.deal())
    if cnum == 1:
        dealer_card = deck.deal()
    else:
        dealer_hidden_card = deck.deal()

# players gonna play

player_scores = dict()
for player in player_list:
    name = player.name
    hand = player_hands[name]
    score = hand.score()
    play = ''
    while score != 'blackjack' and any([score]) <= 21 and play != 'stand':
        play = player.play(hand,player_hands)
        if play == 'hit':
            hand.add_card(deck.deal())
        score = hand.score()
    player_scores[name] = score

player_hand_cards = dict()
for player in player_list:
    player_hand_cards[player.name] = player_hands[player.name].cards

# dealer plays

dealer_hand = bj.Hand([dealer_card,dealer_hidden_card])
score = dealer_hand.score()
play = ''
while score != 'blackjack' and any([score]) <= 21 and play != 'stand':
    play = dealer_player.play(dealer_hand,player_hands)
    if play == 'hit':
        dealer_hand.add_card(deck.deal())
    score = dealer_hand.score()
dealer_hand_cards = dealer_hand.cards
    
# figure out if players won or lost

dealer_score = dealer_hand.score()
#if dealer_score != 'blackjack':
#    temp_score_list = [x for x in dealer_hand.score() if x <=21]
#    dealer_score = max(temp_score_list)
#    


