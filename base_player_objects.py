# basic player classes

# prototype player class

class ProtoPlayer(object):
    
    def __init__(self, name='Proto'):
        self.name = name
        
    def bet(self, table_min, table_max):
        return table_min
    
    def play(self, current_hand, current_table):
        current_score = current_hand.score()
        if current_score == 'blackjack':
            return 'blackjack'
        else:
            return 'stand'
        
# dealer player class
    
class DealerRulesPlayer(ProtoPlayer):
    
    def __init__(self, name='Dealer'):
        self.name = name
          
    def play(self, current_hand, current_table):
        current_score = current_hand.score()
        
        if current_score == 'blackjack':
            return 'blackjack'

        try : # this section is designed for list scores          
 
            # check for must-stand scores
            
            for score in current_score:
                if score > 17 and score <= 21:
                    return 'stand'

            # if we made it here, then dealer must hit

            return 'hit'
            
        except (TypeError): # scalar current_scores go here
        
            if current_score > 17:
                return 'stand'
            else:
                return 'hit'

