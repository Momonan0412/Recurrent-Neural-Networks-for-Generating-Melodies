from keras.layers import Input, LSTM, Dropout, Dense, BatchNormalization
from keras.optimizers import Adam
from keras import regularizers, Model
from constants import *
import os
import tensorflow as tf
from tensorflow.keras.mixed_precision import set_global_policy

# Enable memory fragmentation mitigation
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

# Use mixed precision
# https://keras.io/api/mixed_precision/
set_global_policy('mixed_float16')

# Clear GPU memory
tf.keras.backend.clear_session()

class ModelBuilder:
    def __init__(self):
        pass
    def _build_model(self):
        
        with tf.device('/GPU:0'):
        # Input Layer
            input_layer = Input(shape=(INPUT_SHAPE_ONE))
            
            # First LSTM Layer
            layer_one = LSTM(NUM_UNITS_OR_NUMBER_OF_NEURONS[0], return_sequences=True)(input_layer) # Explicit: This is `Sequence to Sequence` approach
            layer_one = Dropout(0.3)(layer_one)
            
            # # Second LSTM Layer
            layer_two = LSTM(NUM_UNITS_OR_NUMBER_OF_NEURONS[1], return_sequences=False)(layer_one) # Explicit: This is `Sequence to Vector` approach
            layer_two = Dropout(0.2)(layer_two)
            
            # Fully Connected Layer - Dense Layer
            layer_three = Dense(NUM_UNITS_OR_NUMBER_OF_NEURONS[2], activation='relu')(layer_two)
            layer_three = BatchNormalization()(layer_three)
            layer_three = Dropout(0.3)(layer_three)
            
            # Final output layer with softmax activation
            output_layer = Dense(NUMBER_VOCABULARIES_OUTPUT, activation='softmax')(layer_three)
            
            # Compile model
            model = Model(inputs=input_layer, outputs=output_layer)
            model.compile(
                loss=LOSS_OR_ERROR_FUNCTION,
                optimizer=Adam(learning_rate=LEARNING_RATE),
                metrics=[METRICS]
            )
        return model