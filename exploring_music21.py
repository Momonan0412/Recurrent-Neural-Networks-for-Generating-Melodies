from music21 import *
from constants import *
if __name__ == "__main__":
    configure.run()
    melody = converter.parse(FILE_NAME_MIDI)
    melody.show('midi')