from constants import *
from data_handler import *
import numpy as np
class MusicOneHotEncoder:
    def __init__(self):
        self._mappings = StaticDataHandler._load_jsonfile_into_song(MAPPING_PATH)
        self._songs = StaticDataHandler._load_textfile_into_song(DATASET_FILE_PATH)
        pass
    def _convert_songs_to_int(self):
        integer_songs = []
        # Cast songs string to a list
        
        mappings = self._mappings
        # print(type(mappings))
        # mappings = json.loads(mappings)
        songs = self._songs
        songs = songs.split()
        
        # first_symbol = songs[0]
        # print(f"First song symbol: {first_symbol}")
        # print(f"Integer mapping for '{first_symbol}': {mappings.get(first_symbol)}")
        # print(f"Mappings: {mappings}")
        
        for symbol in songs:
            integer_songs.append(mappings[symbol])
        
        # print(integer_songs)
        # for i, symbol in enumerate(songs):
        #     if integer_songs[i] != mappings[symbol]:
        #         print("Does Not Match!")
        
        self._integer_songs = integer_songs
        
    """
    Example with a sequence length of 3:
    Melody: [10, 11, 14, 22, 16, 10, 11, 14, 22, 16, 15, 21, 23]
    
    - First Input: [10, 11, 14], Target: [22]
      This sequence uses the first three notes as context to predict the next note, 22.
      
    - Second Input: [11, 14, 22], Target: [16]
      The next sliding window moves one step forward, using notes 11, 14, and 22 to predict 16.
      
    - Third Input: [14, 22, 16], Target: [10]
      Here, the model learns from notes 14, 22, and 16 to predict 10.

    - Fourth Input: [22, 16, 10], Target: [11]
      This input-target pair continues the pattern, sliding one step forward each time.
    
    - Fifth Input: [16, 10, 11], Target: [14]
    
    - Sixth Input: [10, 11, 14], Target: [22]
      This demonstrates a repeated motif where the same input sequence can appear multiple times
      in the melody, reinforcing the learning of recurring patterns.

    Key Points:
    - Inputs represent previous notes; targets are the next note.
    - Sequence order is preserved to maintain musical structure.
    """
    def _generate_training_sequences(self):
        # 
        self._convert_songs_to_int()
        integer_songs = self._integer_songs
        # e.g., 
        # len(integer_songs) = 100
        # SEQUENCE_LENGTH = 64
        # 100 - 64 = 36
        # There are 36 sets!
        num_sequences = len(integer_songs) - SEQUENCE_STEP
        # print(num_sequences)
        
        data_inputs = []
        data_targets = []
        for i in range(num_sequences):
            data_inputs.append(integer_songs[i: i + SEQUENCE_STEP])
            data_targets.append(integer_songs[i + SEQUENCE_STEP])
            
        self._data_inputs = data_inputs
        self._data_targets = data_targets
        # print(np.array(data_inputs).shape)
        # print(data_inputs[0])
        # print(data_inputs[2])
        
    """
    [[1, 2, 3, 5], [5, 2, 3, 4]]
    =>
    [
      [0, 1, 0, 0, 0, 0],  # 1 -> category index 1 is set to 1
      [0, 0, 1, 0, 0, 0],  # 2 -> category index 2 is set to 1
      [0, 0, 0, 1, 0, 0],  # 3 -> category index 3 is set to 1
      [0, 0, 0, 0, 0, 1],  # 5 -> category index 5 is set to 1
      [0, 0, 0, 0, 0, 1],  # 5 -> category index 5 is set to 1 (same category as before)
      [0, 0, 1, 0, 0, 0],  # 2 -> category index 2
      [0, 0, 0, 1, 0, 0],  # 3 -> category index 3
      [0, 0, 0, 0, 1, 0]   # 4 -> category index 4
    ]
    """
    def one_hot_encode(self): # keras.utils.to_categorical()  
      
      max_input = self._data_inputs_max()
      num_categories = max_input + 1
      sequences = np.array(self._data_inputs)
        
      result = np.zeros((len(sequences), len(sequences[0]), num_categories), dtype=np.uint8)
        
      for i, sequence in enumerate(sequences):
          for j, category in enumerate(sequence):
              result[i, j, category] = 1
      
      input = result
      target = np.array(self._data_targets)
      
      return input, target
      
    def _data_inputs_max(self):
      max_input = max(max(seq) for seq in self._data_inputs)
      return max_input
    
    # def _set_data_and_save_jsonfile(self):
    #   inputs, targets = m.one_hot_encode()
    #   data = {
    #     "inputs" : inputs.tolist(),
    #     "targets" : targets
    #   }
    #   StaticDataHandler._data_to_json_file(JSON_PATH, data)
    def _set_data_and_save_h5file(self):
      inputs, targets = self.one_hot_encode()
      # Guide: data_name, data_set, data_type for `**kwargs`
      h5_config = [
          {'data_name': "inputs", 'data_set': inputs, 'data_type': np.uint8}, # Inputs (one-hot encoded): np.uint8 is optimal.
          {'data_name': "targets", 'data_set': targets, 'data_type': np.uint8}, # Target's max value does not exceed 255.
      ]
      StaticDataHandler._data_to_h5py(H5PY_PATH, config=h5_config)
    
if __name__ == "__main__":
    m = MusicOneHotEncoder()
    m._convert_songs_to_int()
    m._generate_training_sequences()
    m._set_data_and_save_h5file()