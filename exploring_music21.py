# from music21 import *
# if __name__ == "__main__":
#     # configure.run()
#     dicant = corpus.parse('trecento/Fava_Dicant_nunc_iudei')
#     dicant.show()
import tensorflow as tf
if tf.config.list_physical_devices('GPU'):
    print("TensorFlow is using the GPU!")
    
    gpus = tf.config.list_physical_devices('GPU')
    print("Available GPUs:", gpus)
    
    for gpu in gpus:
        details = tf.config.experimental.get_device_details(gpu)
        print("GPU Details:", details)
else:
    print("TensorFlow is using the CPU. ", tf.__version__)