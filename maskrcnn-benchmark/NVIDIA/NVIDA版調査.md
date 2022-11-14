# NVIDIAのmaskrcnn-benchmarkを調査

- [Mask R-CNN for PyTorch](https://catalog.ngc.nvidia.com/orgs/nvidia/resources/mask_r_cnn_for_pytorch)

- [GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Segmentation/MaskRCNN)

- [NGC|CATALOG](https://catalog.ngc.nvidia.com/orgs/nvidia/resources/mask_r_cnn_for_pytorch/files)

## リポジトリ
```
cd O:\src\NVIDIA
git clone https://github.com/NVIDIA/DeepLearningExamples.git
```

## 4つのDockerfile
４つのDockerfileは全て異なる。
```
A "O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\Dockerfile"
B "O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\Dockerfile"
C "O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\docker\Dockerfile"
D "O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\docker\docker-jupyter\Dockerfile"
```
C&Dではpytorch-nightlyが、Cではapexが利用されており、どちらも実験段階（[Automatic Mixed Precision, apex](https://github.com/NVIDIA/apex#1-amp--automatic-mixed-precision)）の古いイメージと思われる。
```
A
ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:21.12-py3

B
ARG FROM_IMAGE_NAME=nvcr.io/nvidia/pytorch:21.12-py3

C
ARG CUDA="9.0"
ARG CUDNN="7"
FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-devel-ubuntu16.04
RUN conda install -y pytorch-nightly -c pytorch \
RUN git clone https://github.com/NVIDIA/apex.git \

D
ARG CUDA="9.0"
ARG CUDNN="7"
FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-devel-ubuntu16.04
RUN conda install -y pytorch-nightly -c pytorch \
```

A vs Bの比較
```
- A -
# Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.
(...)
# openCV
RUN apt-get update && apt-get install -y libgl1-mesa-dev
(...)
COPY pytorch/. .
(...)

- B -
# Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
(...)
      opencv-python==4.4.0.42 \
(...)
COPY . .
(...)
RUN /opt/conda/bin/conda install -y numpys
```
- Bの方がCopyrightの日付が新しい。
- AのコメントにopenCVとあるが、インストールが見当らない。Bにはある。
- pytorchフォルダをCOPYしているのは同じ
- Bではcondaを使用している

## 結論
"O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\Dockerfile"
で検証するのがベストと思われる。