### Tools and Libraries
- **Music21**: A Python library for analyzing and generating music.
- **MuseScore**: Software for music notation.

### Melody Generation Problem
- Treat melody generation as a **time series prediction problem**.
- Use a **vocabulary of notes** to map musical data into sequences.

### Training Process
- Input melody -> **LSTM model** -> Predict next note.

### Melody Generator Process
- Start with a **seed** (initial notes).
- Predict -> Append predicted note -> Feed into model -> Predict (iterative process).

### RNN-LSTM Model
- Melodies have **long-term structural patterns**.
- **LSTMs** are ideal because they capture long-term temporal dependencies.

### Models to Study
- **LSTM (Long Short-Term Memory)**
- **GAN (Generative Adversarial Network)**
- **VAE (Variational Autoencoder)**

### Dataset Used
- **Essen Associative Code and Folksong Database**: [Essen Folk Music Database](http://www.esac-data.org/)


## Music Theory Concepts for Melody Generation in Deep Learning

### Melody Basics
- **Melody**: A sequence of notes and rests that make up the tune of a song.
- **Note** = **Pitch** (how high or low the sound is) + **Duration** (how long the sound lasts).

### Pitch
- Indicates how high or low a sound is.
- In music, higher pitches have higher frequencies.
- On the **musical staff**, the higher the note's position, the higher the pitch.

#### Scientific Pitch Notation
- This notation represents a note by its name and octave (e.g., C3, D4, A1).
- Example: C4 (middle C), where C is the note, and 4 is the octave number.

### MIDI Note Notation
- **MIDI (Musical Instrument Digital Interface)** is a system that helps computers communicate with musical instruments.
- Each note is mapped to a number. For example, C4 = 60.
- MIDI notation is used in deep learning for easy handling of music data.

#### Example: MIDI Note Chart
- C3 = 48
- D3 = 50
- C4 = 60

A complete MIDI note chart can be found at [this reference](https://audiodev.blog/midi-note-chart/).

### Note Values (Durations)
- Music has different note lengths:
  - **Whole note** = 4 beats
  - **Half note** = 2 beats
  - **Quarter note** = 1 beat
  - **Eighth note** = 1/2 beat
  - **Sixteenth note** = 1/4 beat

### Time Signature
- Defines how many beats are in each measure of music:
  - **Top number (numerator)**: Number of beats per measure.
  - **Bottom number (denominator)**: Type of note that gets one beat.
  - Example: 4/4 time means 4 beats per measure, and a quarter note gets 1 beat.

### Key and Tonic
- **Key**: A set of pitches that forms the foundation of a piece of music.
- **Tonic**: The central note or home base that gives a feeling of stability (e.g., C in C major).
- **Modes**: Major (happy) or Minor (sad).
- Example: C major (Cmaj) and A minor (Amin) are key examples.
- There are 24 possible keys (12 notes × 2 modes), but for simplicity, **transpose** all music to Cmaj or Amin.

#### Transposition
- Transposing moves the notes of a piece up or down by a fixed amount.
- **Why transpose to Cmaj or Amin?** This reduces complexity. The musical structure remains the same even though the pitch changes.
- **Why doesn’t transposition change the music's meaning?** Transposition changes pitch but keeps the relative distances between notes the same, so the tune sounds familiar.

### Preprocessing for Deep Learning
1. **Concept of Key**: The neural network learns the key (like Cmaj or Amin) to understand how notes relate to each other.
2. **Melody Generation**: It learns to create melodies that feel coherent by recognizing tension and release (movement between notes and rest) in music.

### Preprocessing Steps
- **Idea 1**: Represent a melody as a sequence of notes:
  - Each note has pitch and duration.
  - Example: [(C4, 1), (D4, 1), (E4, 0.5), (E4, 0.5), (rest, 1)]

- **Idea 2 (Time Series Representation)**:
  - Sample the melody at each **16th note** interval.
  - Each time step represents one 16th note.
  - Use **MIDI numbers** for notes, **"_"** to extend a note, and **"r"** for rest.

#### Example of Time Series Encoding (4/4 Time Signature) of Idea 2
- A 4/4 bar has 16 16th notes (4 beats × 4):

```
[
"60", "_", "_", "_",
"62", "_", "_", "_",
"64", "_", "64", "_",
"65", "_", "62", "_"
]
```
- MIDI numbers represent pitches (C4 = 60).
- The underscore "_" extends a note.
- "r" represents a rest.

### Encoding for Machine Learning
- Convert the time series representation into integers.
- Use **one-hot encoding** to represent each step, making it easier for a model to process.

### Questions
- **Why reduce to 2 keys?** Simplifies learning without losing musical meaning.
- **Does transposition affect sound?** Yes, pitch changes, but the relationship between notes remains consistent.
- **Why does musical content stay the same when transposed?** Because the pattern of intervals (distances between notes) is preserved.
