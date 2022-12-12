"""


"""

import copy
from .player import Player


class Nature():
    
    def __init__(self, config_dict):
        
        # Carrying capacity
        self.organisms_per_gen = config_dict['organisms_per_gen']
        # Frequency of interactions
        self.rounds_per_gen = config_dict['rounds_per_gen']
        # Unit Base
        self.unit_base = config_dict['unit_base']
        # Counter
        self.counter = 0
    
    
    def get_id(self):
        ''' Returns a unique ID for a new Player. '''
        self.counter += 1
        return self.counter
    
    
    def get_organism(self, label=None, strategy=None):
        ''' Generates one organism (a new Player). '''
        if strategy == None:
            strategy = [round(self.unit_base / 3), round(self.unit_base / 3)]
        new_player = Player(self.get_id(), label, self.unit_base, strategy)
        return new_player
    
    
    def create_population(self, number_of_organisms=None, label=None, strategy=None):
        ''' Initializes a population. '''
        if number_of_organisms==None:
            number_of_organisms = self.organisms_per_gen
        
        population = []
        for i in range(number_of_organisms):
            new_player = self.get_organism(label, strategy)
            population.append(new_player)
        return population
    
    
    def get_child(self, parent):
        ''' Produces a mutated child. '''
        # Initialize the child as an identical copy of the parent
        child = copy.deepcopy(parent)
        # Mutate it to make it different from the parent
        child._id = self.get_id()
        child.mutate_strategy()
        return child

    
    def mutate_population(self, population):
        ''' The population is subjected to random mutations. '''
        for organism in population:
            organism.mutate_strategy()











