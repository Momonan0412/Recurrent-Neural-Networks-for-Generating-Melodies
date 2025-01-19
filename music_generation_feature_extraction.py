import os as operating_system
from music21 import converter, note, chord, meter, tempo, pitch, stream, key, interval
from constants import *

class MelodyFeatureExtraction:
    def __init__(self, data_path):
        self._data_path = data_path
        
    def _load_songs_in_kern(self):
        songs = []
        for i, (dirpath, dirnames, filenames) in enumerate(operating_system.walk(self._data_path)):
            for file in filenames:
                if ".krn" in file:
                    path = operating_system.path.join(dirpath, file)
                    song = converter.parse(path)
                    songs.append(song)
        self._songs = songs
        
    """
    Hierarchical Structure: In a musical score, elements are typically nested in layers such as parts, measures, and other containers.
    Accessing notes directly through recurse() searches through all levels of the hierarchy, but this can be slow or overly complex.
    Flattened View: flat.notesAndRests removes the hierarchy, providing a simplified, linear sequence of all note and rest elements in the score or part.
    This makes it easier to loop through the musical content without worrying about nested structures.
    """
    def _has_acceptable_duration(self, song):
        # Access all notes and rests in a flat structure
        for note in song.flat.notesAndRests:
            if note.duration.quarterLength not in ACCEPTABLE_DURATIONS:
                # self._show_songs_parts(song)
                return False
        return True
    
    """
    Print the musical structure of each song in the song list.
    Retrieves songs using `_get_songs()` and prints part names, notes, chords, 
    time signatures, and tempos for each song. Notes and chords display their 
    pitches and durations in quarter-note lengths. Separators are printed between songs.
    Example:
        Part: Soprano
        Note: C4, Duration: 1.0
        Time Signature: 4/4
    Tempo: 120 BPM
    ========================================
    """
    def _show_song_parts(self, song):
        for part in song.parts:
            print(f"Part: {part.partName if part.partName else 'Unnamed Part'}")
            
            # Iterate over elements in the part
            for element in part.recurse():
                if isinstance(element, note.Note):
                    print(type(element.duration.quarterLength))
                    print(f"Note: {element.nameWithOctave}, Pitch: {element.pitch}, Duration: {element.duration.quarterLength}")
                elif isinstance(element, chord.Chord):
                    pitches = [p.nameWithOctave for p in element.pitches]
                    print(f"Chord: {', '.join(pitches)}, Duration: {element.duration.quarterLength}")
                elif isinstance(element, meter.TimeSignature):
                    print(f"Time Signature: {element.ratioString}")
                elif isinstance(element, tempo.MetronomeMark):
                    print(f"Tempo: {element.number} BPM")
    
    def _locate_song_key(self, song):
        parts = song.getElementsByClass(stream.Part)
        for part in parts:
            for measure in part.getElementsByClass(stream.Measure):
                for element in measure:
                    # if isinstance(element, key.KeySignature):
                    if isinstance(element, key.Key):
                        key_signature = element
                        break
                if key_signature:
                    break
            if key_signature:
                self._guess_song_key(song).sharps
                print(f"Found Key Signature: {key_signature.sharps} sharps")
                print(f"Guessed Signature: {self._guess_song_key(song).sharps} sharps")
                print(f"Tonic: {key_signature.tonic.name}")
                if key_signature.mode == 'major':
                    print(f"Mode: {key_signature.mode}")
        if not isinstance(key_signature, key.Key):
            key_signature = self._guess_song_key(song)
        return key_signature
    
    """
    Using:
    'X'maj => Cmaj,
    'Y'min => Amin
    """
    def _transpose(self, _key_signature, _song):
        if _key_signature.mode == "major":
            key_interval = interval.Interval(_key_signature.tonic, pitch.Pitch("C"))
        if _key_signature.mode == "minor":
            key_interval = interval.Interval(_key_signature.tonic, pitch.Pitch("A"))
        transposed_song = _song.transpose(key_interval)
        return transposed_song
    
    """Provides a key `Guess` of the passed song!"""
    def _guess_song_key(self, song):
        key = song.analyze('key')
        # print(f"Key: {key}")
        # tonal_certainty_percentage = key.tonalCertainty() * 100
        # print(f"Tonal Certainty: {tonal_certainty_percentage:.1f}%")
        return key
    
    
    def _preprocess(self):
        self._load_songs_in_kern()
        print("Initial Songs Count: ",len(self._get_songs()))
        new_songs = []
        for song in self._get_songs():
            if self._has_acceptable_duration(song) == False:
                print("Skip!")
                continue
            else:
                print("=" * 40)
                # self._show_song_parts(song)
                new_song = self._transpose(_key_signature = self._locate_song_key(song), _song=song)
                new_songs.append(new_song)
                print("=" * 40)
        self._get_songs()[4].show()
    def _get_songs(self):
        return self._songs
    
if __name__ == "__main__":
    m = MelodyFeatureExtraction(DATASET_PATH)
    m._preprocess()