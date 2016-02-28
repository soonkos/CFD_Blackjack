# basic player classes

# prototype player class

class ProtoPlayer(object):
    
    def __init__(self, name='Proto'):
        self.name = name
        
    def bet(self, current_funds, table_min, table_max):
        return table_min
    
    def play(self, current_hand, current_table):
        return 'stand'
    
    def final_look(self, current_table):
        pass
    
# dealer player class
    
class DealerRulesPlayer(ProtoPlayer):
    
    def __init__(self, name='Dealer'):
        self.name = name
          
    def play(self, current_hand, current_table):
        possible_scores = current_hand.possible_scores()
        
        if possible_scores == 'blackjack':
            return 'stand'

        # check for must-stand scores
            
        for score in possible_scores:
            if 17 <= score and score <= 21:
                return 'stand'

        # if we made it here, then dealer must hit

        return 'hit'