#https://docs.nvidia.com/deeplearning/frameworks/tensorflow-release-notes/index.html
#CUDA 11.0
#pip install tensorflow=2.4.0
#CUDA 11.7
#pip install tensorflow=2.8.3
import sys
import tensorflow as tf

print(f"sys.version => {sys.version}")
print(f"tf.__version__ => {tf.__version__}")

#deprecated
#is_gpu = tf.test.is_gpu_available()
#print(f"tf.test.is_gpu_available() => {is_gpu}")

gpu_devices = tf.config.list_physical_devices('GPU')
print(f"tf.config.list_physical_devices('GPU') =>\n{gpu_devices}")

if len(gpu_devices)>0:
    from tensorflow.python.client import device_lib
    local_devices = device_lib.list_local_devices()
    print(f"device_lib.list_local_devices() =>\n{local_devices}")

    buildinfo = tf.sysconfig.get_build_info()
    cuda_version = buildinfo["cuda_version"]
    cudnn_version = buildinfo["cudnn_version"]
    cpu_compiler = buildinfo["cpu_compiler"]
    cuda_compute_capabilities = buildinfo["cuda_compute_capabilities"]
    print(f'tf.sysconfig.get_build_info()["cuda_version"] => {cuda_version}')
    print(f'tf.sysconfig.get_build_info()["cudnn_version"] => {cudnn_version}')
    print(f'tf.sysconfig.get_build_info()["cpu_compiler"] =>\n{cpu_compiler}')
    print(f'tf.sysconfig.get_build_info()["cuda_compute_capabilities"] =>\n{cuda_compute_capabilities}')
