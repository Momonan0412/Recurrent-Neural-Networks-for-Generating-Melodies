from constants import *
import json
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