DATASET_PATH = "Dataset Melody Generation\\misc_asia" # Dataset Path
SAVE_DIRECTORY = "Processed Dataset"
ACCEPTABLE_DURATIONS = [ # Acceptable Note Duration
    0.25, # 16th Note
    0.5, # 8th Note
    0.75, # Dotted 8th Note
    1.0, # Quarter Note
    1.5, # Dotted Quarter Note
    2.0, # Half Note
    3.0, # 3 Quarter Notes
    4.0  # Whole Note
]
TIME_STEP = 0.25 # 16th Note, using the #2 Idea in preprocessing.