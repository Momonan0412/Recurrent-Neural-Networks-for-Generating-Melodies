import os as operating_system
from music21 import converter, note, chord, meter, tempo, pitch, stream, key, interval, bar
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
        
    """Provides a key `Guess` of the passed song!"""
    def _guess_song_key(self, song):
        key = song.analyze('key')
        # print(f"Key: {key}")
        # tonal_certainty_percentage = key.tonalCertainty() * 100
        # print(f"Tonal Certainty: {tonal_certainty_percentage:.1f}%")
        return key
    
    def _get_song_time_signature(self, song):
        # return song.recurse().getElementsByClass(meter.TimeSignature)[0]
        for ts in song.recurse().getElementsByClass(meter.TimeSignature):
            print(f"Time Signature: {ts.ratioString}")
            
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

    def _get_bar_numbers(self, song):
        barlines = song.recurse().getElementsByClass(bar.Barline)
        if barlines:
            print(f"Found {len(barlines)} barlines in the song.")
        else:
            print("No barlines found in the song.")
          
    def _get_songs(self):
        return self._songs
    
    """
    Note! This Caters to 4/4 Time Signature only!
    TODO: Find A way filter and access the time signatre?
    
    TODO: IMPLEMENT! OR FIND A WAY TO! TIME SIGNATURE MAKER? Or?
    
    Using the Idea #2 - A Time Series Representation
    Using the 16th note's duration which is 0.25 as a time-step
    Use MIDI numbers for notes, "_" to extend a note, and "r" for rest.
    Format Example:
        [
            "60", "_", "_", "_",
            "62", "_", "_", "_",
            "64", "_", "64", "_",
            "65", "_", "62", "_"
        ]    
    - MIDI numbers represent pitches (C4 = 60).
    - The underscore "_" extends a note.
    - "r" represents a rest.
    
    time_step == 16th note
    """
    def _encode_song_as_time_series(self, song):
        # Example: Note with pitch = 60, duration = 1.0
        # List[60,"_","_","_",] Where in the list each Item corresponds to a 16th note
        # 4 * .25 = 1.0
        # List[x,"_","_","_",] 16th note
        # List[x,"_"] 8th note
        # List[x] Whole note
        encoded_song = []
        for event in song.flat.notesAndRests:
            # print(event)
            # Handle Notes
            if isinstance(event, note.Note):
                symbol = event.pitch.midi
            # Handle Rests
            if isinstance(event, note.Rest):
                symbol = 'r'
            # Convert note/rest into time series notation
            steps = int(event.duration.quarterLength / TIME_STEP)
            
            for step in range(steps):
                if step == 0:
                    encoded_song.append(symbol)
                else:
                    encoded_song.append('_')
                    
        encoded_song = " ".join(map(str, encoded_song))
        # print(encoded_song)
        return encoded_song
    
    def _save_song_into_textfile(self, save_path, encode_song):
        with open(save_path, 'w') as fp:
            fp.write(encode_song)
    
    def _preprocess(self):
        self._load_songs_in_kern()
        for index, song in enumerate(self._get_songs()):
            if self._has_acceptable_duration(song):
                transposed_song = self._transpose(self._locate_song_key(song), song)
                encode_song = self._encode_song_as_time_series(transposed_song)
                save_path = operating_system.path.join(SAVE_DIRECTORY, str(index))
                self._save_song_into_textfile(save_path, encode_song)
    
if __name__ == "__main__":
    m = MelodyFeatureExtraction(DATASET_PATH)
    m._preprocess()