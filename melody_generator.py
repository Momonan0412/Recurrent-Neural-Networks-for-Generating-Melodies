from keras import Model
from keras.api.utils import to_categorical
from keras.api.models import load_model
from constants import *
from data_handler import StaticDataHandler
from m_simulated_annealing import SimulatedAnnealing
from melody_temperature_sampling import TemperatureSampling
import numpy as np
class MelodyGenerator:
    def __init__(self, model_path=MODEL_PATH):
        self._model_path = model_path
        self._load_model()
        self._load_mapped_vocabularies()
        self._set_start_symbols()
        self._temperature_sampling = TemperatureSampling()
        
    def _load_model(self):
        self._model = load_model(self._model_path)
    
    def _load_mapped_vocabularies(self):
        self._mapped_vocabularies = StaticDataHandler._load_jsonfile_into_song(MAPPING_PATH)
    
    # "Main" Function
    """
    seed => piece of melody, passed to the model and model would continue base on the seed
    seed => "64_ 63_ _"
    """
    def _generate_melody(self, seed, num_of_steps, max_sequence_length = SEQUENCE_STEP):
        # Create seed with start symbols
        seed = seed.split()
        melody = seed
        
        seed = self._get_start_symbols() + seed
        
        seed = self._set_seed_to_int(seed)
        
        
        for _ in range(num_of_steps):
            seed = seed[-max_sequence_length : ]
            # print(seed)
            # # Guide
            # one_hot_seed_test = to_categorical(seed, num_classes=len(self._get_mapped_vocabularies()))
            one_hot_seed = StaticDataHandler._one_hot_encode(np.array(seed), len(self._get_mapped_vocabularies()))
            one_hot_seed = one_hot_seed[np.newaxis, ...]
            
            probabilities = self._get_model().predict(one_hot_seed)[0]
            
            self._temperature_sampling._set_temperature(TEMPERATURE_SAMPLING)
            self._temperature_sampling._set_probability_list(probabilities)
            result = self._temperature_sampling._sample_with_temperature()
            
            seed.append(result)
            
            # print(result)
            
            # for key, value in self._get_mapped_vocabularies().items():
            #     if value == result:
            #         result_symbol = key
            
            result_symbol = [key for key, value in self._get_mapped_vocabularies().items() if value == result][0]
            # print(result_symbol)
            # print(type(result_symbol))
            
            if result_symbol == '/':
                # print("Mmkay!")
                break
            
            melody.append(result_symbol)
            # print(melody)
            
        return melody
            
    # Set
    def _set_seed_to_int(self, seed):
        # seed = seed.split() # Debugging
        map_seed = [self._get_mapped_vocabularies()[symbol] for symbol in seed]
        # for symbol in seed:
        #     map_seed.append(self._get_mapped_vocabularies()[symbol])
        return map_seed
    def _set_start_symbols(self):
        self._start_symbols = ["/"] * SEQUENCE_LENGTH_DELIMITER # SAME IDEA WHEN CONVERTING THE INPUT DATA WITH "SEQUENCE_LENGTH_DELIMITER"
    
    # Get
    def _get_mapped_vocabularies(self):
        return self._mapped_vocabularies
    
    def _get_start_symbols(self):
        return self._start_symbols
    
    def _get_model(self):
        return self._model
        
    
if __name__ == "__main__":
    mg = MelodyGenerator()
    seed = "64 _ 69 _ _ _ 71 _ 72"
    # print(mg._get_mapped_vocabularies())
    melody = mg._generate_melody(seed=seed,num_of_steps=500)
    print(melody)