# try to create a basic blackjack game

import blackjack_base as bj
import blackjack_base_players as bj_player

# create the players

player1 = bj_player.ProtoPlayer(name='Steve')
player2 = bj_player.ProtoPlayer(name='Jenny')
player3 = bj_player.DealerRulesPlayer(name='David')
player4 = bj_player.DealerRulesPlayer(name='Lauren')
player_list = [player1, player2, player3, player4]

# set table minimum and maximum and the starting funds for each player

table_minimum = 10.0
table_maximum = 100.0
starting_funds = 100.0

# initialize game

game = bj.Game(player_list, table_minimum, table_maximum, starting_funds)

# play until all players have lost all their money or until maximum number of 
# rounds have been played

num_rounds_max = 1000

while game.player_list and game.round_counter < num_rounds_max:
    game.ask_for_bets()
    game.deal_starting_cards()
    for player in player_list:
        game.play_hand(player)
    game.dealer_play_hand()
    game.settle_bets()
    game.final_look_at_table()

print game.player_funds
print game.player_rounds_played

