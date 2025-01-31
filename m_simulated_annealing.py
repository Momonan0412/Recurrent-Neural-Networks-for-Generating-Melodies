import numpy as np
from constants import *
import random
class SimulatedAnnealing:
    @staticmethod
    def _objective_funcion(index, list_probabilities):
        return -1 * list_probabilities[index]
    
    @staticmethod
    def _run(list_probabilities):
        
        # Generate `current index` using rand
        current_index = random.randint(0, len(list_probabilities) - 1)
        # Use Objective Function and pass the generated `current index`
        current_value = SimulatedAnnealing._objective_funcion(current_index, list_probabilities)
        
        T = TEMPERATURE
        cool_rate = COOLING_RATE
        
        while T > 0.001:
            
            # Generate new index using rand
            
            new_index = random.randint(0, len(list_probabilities) - 1)
            # Use Objective Function and pass the generated new index to get the `new value`
            new_value = SimulatedAnnealing._objective_funcion(new_index, list_probabilities)
            
            # Calculate Delta;    
            delta = new_value - current_value
            
            # if delta value is less than zero then the new value and index is better
            
            # https://en.wikipedia.org/wiki/Boltzmann_distribution, ???? Wala ko kasabut
            # or, to escape the `local minima`,
            #  np.exp(-delta / T) > random.random which gives between range of 0 to 1
            # v = np.exp(-delta / T)
            # r = random.random()
            if delta < 0 or np.exp(-delta / T) > random.random():
                current_value = new_value
                current_index = new_index
            
            T *= cool_rate        
            
        return list_probabilities[current_index]