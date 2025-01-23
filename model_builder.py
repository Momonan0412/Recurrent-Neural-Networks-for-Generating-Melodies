from keras.api.layers import Input, LSTM, Dropout, Dense
from keras.api.optimizers import Adam
from keras import regularizers, Model
from constants import *
class ModelBuilder:
    def __init__(self):
        pass
    def _build_model(self):
        input = Input(shape=(INPUT_SHAPE_ONE))
        layer_one = LSTM(NUM_UNITS_OR_NUMBER_OF_NEURONS[0], return_sequences=True)(input) # Explicit: This is `Sequence to Sequence` approach
        layer_two = LSTM(NUM_UNITS_OR_NUMBER_OF_NEURONS[1], return_sequences=False)(layer_one) # Explicit: This is `Sequence to Vector` approach
        layer_two = Dropout(0.2)(layer_two)
        output = Dense(NUMBER_VOCABULARIES_OUTPUT, activation='softmax')(layer_two)
        model = Model(inputs=input, outputs=output)
        model.compile(
            loss=LOSS_OR_ERROR_FUNCTION,
            optimizer=Adam(learning_rate=LEARNING_RATE),
            metrics=[METRICS]
        )
        return model