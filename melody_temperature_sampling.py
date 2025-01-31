import numpy as np

class TemperatureSampling:
    """
    Temperature:
    - If **temperature → ∞ (very high)**, the probability distribution becomes nearly uniform.
    - Every choice has almost the same probability → **Fully random (Non-Deterministic)**
    
    - If **temperature → 0** (very low), the highest probability choice dominates.
    - The model picks the most probable value **almost always** → **Fully Deterministic**
    
    - If **temperature = 1**, the probabilities remain unchanged from the original softmax distribution.
    - **Balances randomness and structure** (default behavior).
    """
        
    def _sample_with_temperature(self):
        
        # logarithms transform very small numbers into manageable values 
        # (more negative, but still within a range that the computer can handle).
        # taking the log of the probabilities and dividing by the temperature it 
        # adjust the "sharpness" of the probability distribution, and we also avoid numerical instability.
        predictions = np.log(self._probability_list) / self._temperature
        # print(np.sum(predictions))
        
        # The softmax function normalizes a vector of values 
        # (like a list of logits or raw predictions) to make them probabilities that sum to 1.
        probabilties = self._softmax_function(predictions)
        # print(np.sum(probabilties))

        choices = range(len(probabilties))
        # print(choices)
        index = np.random.choice(choices, p=probabilties)
        # print(index)
        return index
        
    def _softmax_function(self, log_predictions):
        exp_x = np.exp(log_predictions)
        return exp_x / np.sum(exp_x)
    
    def _set_probability_list(self, probability_list):
        self._probability_list = probability_list
        
    def _set_temperature(self, temperature):
        self._temperature = temperature
        
if __name__ == "__main__":
    arr = np.array([1.0164203e-04, 4.6664529e-05, 9.2410349e-04, 4.6209168e-02, 2.6603891e-03,
                        1.5857868e-04, 1.7733490e-05, 4.1236499e-04, 1.0189359e-04, 6.2514201e-02,
                        1.7849683e-05, 3.2243662e-04, 2.1386104e-05, 2.4572229e-02, 7.1056312e-01,
                        5.0517679e-03, 2.0676316e-05, 2.2737615e-05, 3.8654129e-03, 1.9599256e-05,
                        3.7627822e-05, 6.0298142e-05, 1.7885124e-05, 1.2993868e-04, 8.7122302e-05,
                        5.4138403e-05, 1.7918452e-05, 3.2454042e-05, 1.8304232e-05, 2.1443613e-05,
                        4.9901549e-02, 1.7749733e-05, 2.0459765e-05, 2.1410264e-05, 2.7463653e-05,
                        4.0219973e-05, 5.7445090e-02, 2.6517883e-02, 1.4502298e-03, 3.5930790e-03,
                        2.6827370e-04, 9.1420190e-04, 3.2026932e-04, 1.2747947e-03, 8.6286171e-05])


    ts = TemperatureSampling(probability_list=arr, temperature=1.8)
    ts._sample_with_temperature()