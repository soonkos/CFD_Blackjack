# try to create a basic blackjack game

import base_blackjack_objects as bj
import base_player_objects as bj_player

# create deck

deck = bj.Deck()

# create the dealer

dealer_player = bj_player.DealerRulesPlayer()

# create the players

player1 = bj_player.ProtoPlayer(name='Steve')
player2 = bj_player.ProtoPlayer(name='Jenny')
player3 = bj_player.DealerRulesPlayer(name='David')
player4 = bj_player.DealerRulesPlayer(name='Lauren')
player_list = [player1, player2, player3, player4]

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

player_starting_hand_cards = dict()
for player in player_list:
    player_starting_hand_cards[player.name] = player_hands[player.name].cards[:]

player_possible_scores = dict()
player_best_scores = dict()
for player in player_list:
    name = player.name
    hand = player_hands[name]
    scores = hand.possible_scores()
    play = ''
    while scores != 'blackjack' \
          and any(x <= 21 for x in scores) \
          and play != 'stand':
        play = player.play(hand,player_hands)
        if play == 'hit':
            hand.add_card(deck.deal())
        scores = hand.possible_scores()
    player_possible_scores[name] = scores
    player_best_scores[name] = hand.best_score()

player_hand_cards = dict()
for player in player_list:
    player_hand_cards[player.name] = player_hands[player.name].cards

# dealer plays

dealer_hand = bj.Hand([dealer_card,dealer_hidden_card])
scores = dealer_hand.possible_scores()
play = ''
while scores != 'blackjack' \
      and any(x <= 21 for x in scores) \
      and play != 'stand':
    play = dealer_player.play(dealer_hand,player_hands)
    if play == 'hit':
        dealer_hand.add_card(deck.deal())
    scores = dealer_hand.possible_scores()
    
dealer_hand_cards = dealer_hand.cards
dealer_possible_scores = dealer_hand.possible_scores()
    
# figure out if players won or lost

dealer_score = dealer_hand.best_score()
for player in player_list:
    name = player.name
    hand = player_hands[name]
    score = hand.best_score()
    bet = player_bets[name]
    if score == 'blackjack':
        player_funds[name] += 1.5*bet
    elif score == 'bust':
        player_funds[name] -= bet
    else:
        if dealer_score == 'blackjack':
            player_funds[name] -= bet
        elif dealer_score == 'bust':
            player_funds[name] += bet
        else:
            if score > dealer_score:
                player_funds[name] += bet
            elif score < dealer_score:
                player_funds[name] -= bet
            else:
                pass




