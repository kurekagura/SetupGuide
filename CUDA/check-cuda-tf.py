#CUDA 11.0
#pip install tensorflow=2.40
import sys
import tensorflow as tf

print(f"sys.version => {sys.version}")
print(f"tf.__version__ => {tf.__version__}")

#deprecated
#is_gpu = tf.test.is_gpu_available()
#print(f"tf.test.is_gpu_available() => {is_gpu}")

gpu_devices = tf.config.list_physical_devices('GPU')
print(f"tf.config.list_physical_devices('GPU') => \n{gpu_devices}")

if len(gpu_devices)>0:
    from tensorflow.python.client import device_lib
    local_devices = device_lib.list_local_devices()
    print(f"device_lib.list_local_devices() => \n{local_devices}")
