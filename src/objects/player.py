"""


"""

import random
import numpy as np


class Player():
    
    def __init__(self, _id : int, label : str, base : int, strategy : list):
        ''' Initializes an object of class Player. '''
        
        # Id
        self._id = _id
        
        # Label
        self.label = label
        
        # Unit base
        self.base = base
        
        # Strategy
        self.R = strategy[0]
        self.S = strategy[1]
        self.P = round(self.base - self.R - self.S)

        # Fitness
        self.fitness = 0
    
    
    def play(self):
        ''' Chooses R/S/P with probabilities defined by the strategy. '''
        return random.choices(['R','S','P'], weights=(self.R, self.S, self.P))[0]
    
    
    def play_single_match(self, opponent, payoff_mat):
        ''' Play a match against an opponent.
        The two payoff values for the two players are returned. '''
        return payoff_mat.get_payoff(self.play(), opponent.play())
    
    
    def get_expected_value_of_the_match(self, opponent, payoff_mat):
        ''' Computes the expected value of a match given the strategies of the
        two players. Used when running in "deterministic" mode.
        '''
        # Payoff matrix
        payoff_mat = np.array(payoff_mat.payoff_matrix)
        
        # Probabilities matrix (probabilities of each possible match)
        prob_mat = self.get_event_probabilities_from_encounter(opponent)
        
        # Weigthed payoffs (by element-wise multiplication of payoffs with
        # their probability)
        weighted_payoff_mat = np.multiply(payoff_mat, prob_mat)
        
        expected_value = weighted_payoff_mat.sum()
        
        return expected_value
    
    def get_event_probabilities_from_encounter(self, opponent):
        ''' Compute probability of each possible match, given the strategies of
        the two players. This function is used to compute the expected value of
        a match (when using the "deterministic" mode).
        '''
        weights_1 = [self.R, self.S, self.P]
        weights_2 = [opponent.R, opponent.S, opponent.P]
        
        weights_matrix = []
        for w1 in weights_1:
            row = []
            for w2 in weights_2:
                row.append(w1 * w2)
            weights_matrix.append(row)
        
        # To numpy ndarray
        weights_matrix = np.array(weights_matrix)
        
        # Convert weights to probabilities
        weights_matrix = weights_matrix / self.base**2
        
        return weights_matrix
        
    def challenge_all(self, opponents, payoff_mat, method):
        ''' The individual challenges every other Player in the population.
        Its cumulative_fitness is the sum of the payoffs from all the games played.
        
        When method is "stochastic", every game consist of a single match where both
        players choose their move probabilistically, according to their strategy.
        
        When method is "deterministic", every game returns the expected value of the
        payoff for the undividual, given its strategy and the strategy of the opponent.
        '''
        cumulative_fitness = 0
        for opponent in opponents:
            
            #results = payoff_mat.get_payoff(self.play(), opponent.play())
            if method == "stochastic":
                results = self.play_single_match(opponent, payoff_mat)
                payoff = results[0]
            
            elif method == "deterministic":
                payoff = self.get_expected_value_of_the_match(opponent, payoff_mat)
            
            cumulative_fitness += payoff
        
        return cumulative_fitness


    def mutate_strategy(self, quantity = 1):
        ''' Mutate the strategy. Two out of {'R','S','P'} are randomly chosen
        to be a "donor" and an "acceptor". Then, a quantity is subtracted to the
        donor and added to the acceptor. '''
        
        # Randomly chose donor and acceptor
        donor, acceptor = random.sample(['R', 'S', 'P'], 2)
        
        # Check that the donor doesn't become negative
        if self.is_valid_mutation(donor, quantity):
            # Transfer that quantity from donor to acceptor
            self.change_weight(donor, amount = -quantity)
            self.change_weight(acceptor, amount = quantity)
    
    
    def change_weight(self, item: str, amount: int):
        ''' Adds  amount  to the choice specified by  item. This function is
        used when mutating the strategy of a Player. '''
        
        if item == 'R':
            self.R += amount
        elif item == 'S':
            self.S += amount
        elif item == 'P':
            self.P += amount
    
    def is_valid_mutation(self, donor, subtrahend):
        ''' Checks that the donor doesn't become negative. '''
        return vars(self)[donor] - subtrahend >= 0
        
        # if donor == 'R':
        #     return self.R - subtrahend >= 0
        # elif donor == 'S':
        #     return self.S - subtrahend >= 0
        # elif donor == 'P':
        #     return self.P - subtrahend >= 0




















