import music21 as m21
from constants import *
from data_handler import StaticDataHandler
class MelodyToMIDIConverter:
    def __init__(self, melody):
        self._melody = melody
        
    def _save_melody(self):
        self._m21_stream.write(FORMAT_MIDI, FILE_NAME_MIDI)
    
    def _create_m21_stream(self):
        # Notes: m21 containers => parse, measure, etc.
        m21_stream = m21.stream.Stream()
        self._m21_stream = m21_stream
    
    def _melody_parse_symbols(self):
        self._create_m21_stream()
        
        melody = self._melody
        m21_stream = self._get_m21_stream()
        
        start_symbol = None
        step_counter = 1
        for symbol in melody:
            if symbol != "_":
                
                if start_symbol is not None:
                    ####
                    m21_event = self._melody_parse_symbols_helper(step_counter, start_symbol)
                    ####
                    # # Debugging    
                    # print(start_symbol)
                    
                    m21_stream.append(m21_event)
                    step_counter = 1
                
                start_symbol = symbol
                
            else:
                step_counter += 1
            
        if start_symbol is not None:
            ####
            m21_event = self._melody_parse_symbols_helper(step_counter, start_symbol)
            m21_stream.append(m21_event)
            ####
        # Debugging      
        m21_stream.show('text')
        
        self._m21_stream = m21_stream
        
    def _melody_parse_symbols_helper(self, step_counter, start_symbol):
        quarter_note_duration = TIME_STEP * step_counter # .25 * step_counter
        if start_symbol == "r":
            m21_event = m21.note.Rest()
        else:
            m21_event = m21.note.Note(int(start_symbol))
        m21_event.duration.quarterLength = quarter_note_duration
        self._m21_note_details(m21_event)
        return m21_event
    
    def _create_notes_rest_objects(self):
        pass
    
    def _get_m21_stream(self):
        return self._m21_stream
    
    def _m21_note_details(self, m21_event):
        print("Quarter Length Duration: ", m21_event.duration.quarterLength)
        print("Duration Type: ", m21_event.duration.type)
        if m21_event.isNote:
            print("Note's name: ", m21_event.nameWithOctave)
        elif m21_event.isRest:
            print("A 'Rest'")
        
if __name__ == "__main__":
    melody = StaticDataHandler._load_jsonfile_into_song(GENERATED_MELODY_PATH)
    # print(melody)
    m_to_midi = MelodyToMIDIConverter(melody)
    m_to_midi._melody_parse_symbols()
    m_to_midi._save_melody()