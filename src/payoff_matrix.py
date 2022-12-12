"""



"""

import pandas as pd


class PayoffMatrix():
    
    def __init__(self, config_dict):
        ''' Initializes an object of class PayoffMatrix. '''
        
        # Dataframe from 2D list
        self.payoff_matrix = pd.DataFrame(config_dict['payoff'])
        
        # Check that the matrix has been specified correctly
        if self.payoff_matrix.shape != (3, 3):
            raise Exception("Payoff matrix must be 3x3")
        
        # Set rows and columns names
        self.payoff_matrix.index = ['R', 'P', 'S']
        self.payoff_matrix.columns = ['R', 'P', 'S']
    
    
    def get_payoff(self, first_player_choice, second_player_choice):
        ''' Returns the two payoffs (for the two Players). '''
        return (
            self.payoff_matrix.loc[first_player_choice, second_player_choice],
            self.payoff_matrix.loc[second_player_choice, first_player_choice])










