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