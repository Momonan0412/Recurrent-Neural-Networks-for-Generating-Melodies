from constants import *
import json
import h5py
import numpy as np

class StaticDataHandler:
    @staticmethod
    def _load_textfile_into_song(text_file_path):
        with open(text_file_path, 'r') as fp:
            return fp.read()
    @staticmethod
    def _mapping_vocabulary_to_json(mapping_vocabulary):
        with open(MAPPING_PATH, 'w') as fp:
            json.dump(mapping_vocabulary, fp, indent=4)
    @staticmethod
    def _save_song_s_into_textfile(self, save_path, _song_s):
        with open(save_path, 'w') as fp:
            fp.write(_song_s)        
    @staticmethod
    def _data_to_h5py(h5py_path, **kwargs):
        """
        Save datasets to an HDF5 file.

        Parameters:
        - h5py_path (str): Path to the HDF5 file.
        - **kwargs: Configuration dictionary with 'config' key containing a list of dataset info.
        Each dataset info must have:
            - 'data_name': Name of the dataset in the HDF5 file.
            - 'data_set': Numpy array or list to be saved.
            - 'data_type': Data type for storage (e.g., int, float).
        """
        with h5py.File(h5py_path, 'w') as h5_file:
            # Save each dataset based on configuration
            for h5_config in kwargs.get('config', []):
                h5_file.create_dataset(
                    h5_config['data_name'], 
                    data=np.array(h5_config['data_set'], dtype=h5_config['data_type'])
                )