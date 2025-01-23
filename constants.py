KERN_DATASET_PATH = "Dataset Melody Generation" # Dataset Path
SAVE_DIRECTORY = "Processed Dataset"                  # Processed Dataset
INITIAL_PROCESSED_DATASET_PATH = "Processed Dataset"  # Processed Dataset
DATASET_FILE_PATH = "Processed Dataset\\Combined Dataset\\combined_dataset"
ACCEPTABLE_DURATIONS = [                              # Acceptable Note Duration
    0.25,                                             # 16th Note
    0.5,                                              # 8th Note
    0.75,                                             # Dotted 8th Note
    1.0,                                              # Quarter Note
    1.5,                                              # Dotted Quarter Note
    2.0,                                              # Half Note
    3.0,                                              # 3 Quarter Notes
    4.0                                               # Whole Note
]
TIME_STEP = 0.25                                      # 16th Note, using the #2 Idea in preprocessing.
SEQUENCE_LENGTH_DELIMITER = 64                        # Doesn't directly influence how the LSTM/RNN works in terms of sequence processing.
SEQUENCE_STEP = 64                                    # This Matters WTF?
MAPPING_PATH = "mapped_vocabularies.json"             # Path to store the mapped vocabularies into json.
H5PY_PATH = "dataset.h5"                              # Path to store the h5 file.


"""
SO, WHAT SHOULD I USED, UNSA NA SHAPE! TASUKETE!
BASED ON THE PREPROCESS AND SHAPES?
PREPROCESSED:
CATER'S 4/4 TIME SIGNATURE NOTES TO STRING
NOTES MAPPED WITH LENGTH 46
STRING TO INTEGER BASED ON THE MAPPED VALUE
INTEGER LIST ONE HOT ENCODED
"""
INPUT_SHAPE_ONE = (None, 46)                          # Based on the 'SINGLE SAMPLE INPUT''s shape
INPUT_SHAPE_TWO = (64, 46)                            # Based on the 'SINGLE SAMPLE INPUT''s shape, 64 here is the @SEQUENCE_STEP

NUMBER_VOCABULARIES_OUTPUT = 46                       # Based on the # of `mapped_vocabularies`

LOSS_OR_ERROR_FUNCTION = "sparse_categorical_crossentropy"
METRICS = "sparse_categorical_accuracy"
                                                      # https://keras.io/api/losses/
NUM_UNITS_OR_NUMBER_OF_NEURONS = [256, 128]           # Number of neurons
LEARNING_RATE = 0.001                                 # Learning Rate... dot .. dot .
BATCH_SIZE = 64                                       # Before backpropagation this should be met first
NUMBER_EPOCH = 50 
