"""

"""

import json
import random
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from objects.nature import Nature
from objects.payoff_matrix import PayoffMatrix


# The config file
JSON_CONFIG_FILENAME = "config.json"


# Define Functions

def read_json_file(filename: str) -> dict:
    ''' JSON file to dictionary. '''
    with open(filename) as json_content:
        return json.load(json_content)


def get_population_stats(population, config_dict):
    ''' Returns the population statistics for R, S and P. The quantities from the
    strategies of all the organisms in the population are considered. Then, the
    frequencies of the three choices are returned.
    '''
    cum_R = 0
    cum_S = 0
    cum_P = 0
    
    for org in population:
        cum_R += org.R
        cum_S += org.S
        cum_P += org.P
    
    total = config_dict['organisms_per_gen'] * config_dict['unit_base']
    
    freq_R = cum_R / total
    freq_S = cum_S / total
    freq_P = cum_P / total
    
    return [freq_R, freq_S, freq_P]


def print_stats(stats, generation):
    ''' Prints the statistics from  get_population_stats  to standard output. '''
    
    print("Generation {}:\t{:.4f}\t{:.4f}\t{:.4f}".format(
        generation, stats[0], stats[1], stats[2]))


def save_plot(global_stats_dictionary, filename):
    ''' Saves a plot for the global statistics to PNG file. '''
    plt.figure(figsize=(16, 9))
    plt.ylim((0, 1))
    plt.plot(global_stats_dictionary['R'], label='R')
    plt.plot(global_stats_dictionary['S'], label='S')
    plt.plot(global_stats_dictionary['P'], label='P')
    plt.legend()
    plt.savefig(filename, dpi=300)
    plt.show()


def check_dir_path(dir_path):
    ''' If the directory at the specified path doesn't exists, it's created.
    Any missing parent directory is also created. If the directory already
    exists, it is left un modified. '''
    os.makedirs(dir_path, exist_ok=True)


def main():
    
    # Read config file and make a dictionary
    config = read_json_file(JSON_CONFIG_FILENAME)
    
    # Set up path where results are going to be stored
    sim_results_dir_path = os.path.join('../results', time.strftime("%Y%m%d%H%M%S"))
    check_dir_path(sim_results_dir_path)
    
    # Instantiate Nature object
    nature = Nature(config)
    
    # Instantiate PayoffMatrix object
    payoff_matrix = PayoffMatrix(config)
    
    # Set method
    METHOD = config["method"]
    
    # Number of generations before stopping simulation
    NUMBER_OF_GEN = config["number_of_generations"]
    
    global_stats = []
    
    generation = 0
    
    # Generate starting population
    population = nature.create_population()
    
    # Stats for generation 0
    stats = get_population_stats(population, config)
    global_stats.append(stats)
    
    # Initialize standard output
    print("\t\tR\tS\tP")
    
    # Print stats for generation 0 and raise counter
    print_stats(stats, generation)
    generation += 1
    
    while generation < NUMBER_OF_GEN:
        
        mutants = [nature.get_child(parent) for parent in population]
        
        # Evaluate the organisms' strategies
        for i in range(len(population)):
            
            # Define challenger
            challenger = population[i]
            # All the other players are challenged
            opponents = [population[j] for j in range(len(population)) if j!=i]
            # Make the challenger play with all the opponents
            score = challenger.challenge_all(opponents, payoff_matrix, METHOD)
            # Assign fitness to the challenger
            challenger.fitness = score
            # Define mutant challenger
            mut_challenger = mutants[i]
            # Make the mutant challenger play with the same opponents
            mut_score = mut_challenger.challenge_all(opponents, payoff_matrix, METHOD)
            # Assign fitness to the mutant challenger
            mut_challenger.fitness = mut_score
        
        
        # Natural selection
        new_population = []
        for i in range(len(population)):
            parent = population[i]
            child = mutants[i]
            
            if parent.fitness > child.fitness:
                new_population.append(parent)
            elif child.fitness > parent.fitness:
                new_population.append(child)
            else:
                # In case of a tie, throw a coin
                if random.random() > 0.5:
                    new_population.append(parent)
                else:
                    new_population.append(child)
        
        # Over-write population
        population = new_population
        
        # Stats for this generation
        stats = get_population_stats(population, config)
        global_stats.append(stats)
        
        print_stats(stats, generation)
        generation += 1
    
    
    global_stats_df = pd.DataFrame(global_stats)
    global_stats_df.columns = ["R", "S", "P"]
    
    global_stats_dict = global_stats_df.to_dict('list')
    
    # Write global stats to json file
    outfilepath = sim_results_dir_path + "/global_stats.json"
    with open(outfilepath, "w") as json_file:
        json.dump(global_stats_dict, json_file)
    
    # Save plot
    outfilepath = sim_results_dir_path + "/lineplot.png"
    save_plot(global_stats_dict, outfilepath)


# Entry point for program execution
if __name__ == "__main__":
    
    main()











