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

# Setup Instruction
[More]->[Setup] [->here](https://catalog.ngc.nvidia.com/orgs/nvidia/resources/mask_r_cnn_for_pytorch/setup)

# Inspect

## nvcr.io/nvidia/pytorch:21.12-py3

```
docker pull nvcr.io/nvidia/pytorch:21.12-py3
docker inspect nvcr.io/nvidia/pytorch:21.12-py3
```

```
"PATH=
/opt/conda/lib/python3.8/site-packages/torch_tensorrt/bin:
/opt/conda/bin:
/usr/local/mpi/bin:
/usr/local/nvidia/bin:
/usr/local/cuda/bin:
/usr/local/sbin:/usr/local/bin:
/usr/sbin:/usr/bin:/sbin:
/bin:/usr/local/ucx/bin:
/opt/tensorrt/bin",

"CUDA_VERSION=11.5.0.029",
"CUDA_DRIVER_VERSION=495.29.05",
"_CUDA_COMPAT_PATH=/usr/local/cuda/compat",
"CUDNN_VERSION=8.3.1.22",

"PYTORCH_BUILD_VERSION=1.11.0a0+b6df043",
"PYTORCH_VERSION=1.11.0a0+b6df043",
```

## Summary

- Python3.8
- CUDA11.5
- CUDNN_VERSION=8.3
- PyTorch1.11

# [Quick Start Guide](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Segmentation/MaskRCNN#setup)

```
git clone https://github.com/NVIDIA/DeepLearningExamples.git
cd DeepLearningExamples/PyTorch/Segmentation/MaskRCNN
```

```
./download_dataset.sh <data/dir>
#要約
#COCO 2017 dataset（3つのzip）のwget
#coco_annotations_minival.tgzのwget
```
- [train2017.zip](http://images.cocodataset.org/zips/train2017.zip)
- [val2017.zip](http://images.cocodataset.org/zips/val2017.zip)
- [annotations_trainval2017.zip](http://images.cocodataset.org/annotations/annotations_trainval2017.zip)
- [coco_annotations_minival.tgz](https://dl.fbaipublicfiles.com/detectron/coco/coco_annotations_minival.tgz)・・・FB（detectronプロジェクト）からの配布物?

以下はCOCO 2017 datasetの４点セットであるが、スクリプトにもなく必須ではない。
- [test2017.zip](http://images.cocodataset.org/zips/test2017.zip)

```
cd pytorch/
bash scripts/docker/build.sh
#要約
#docker build --rm -t nvidia_joc_maskrcnn_pt . -f Dockerfile
```
- pytorch\Dockerfileを使ったdocker build。

- --rm:Remove intermediate containers after a successful build (default true)

コンテナイメージが完成後、
```
bash scripts/docker/interactive.sh <path/to/dataset/>

~内容~
#!/bin/bash

PATH_TO_COCO=$1
MOUNT_LOCATION='/datasets/data'
NAME='maskrcnn_interactive'
docker run --runtime=nvidia -v $PATH_TO_COCO:/$MOUNT_LOCATION \
    --rm --name=$NAME \
    --shm-size=10g --ulimit memlock=-1 --ulimit stack=67108864 \
    --ipc=host \
    -t -i nvidia_joc_maskrcnn_pt bash
```
- -t : Allocate a pseudo-TTY, -i : Keep STDIN open even if not attached
- --rm : Automatically remove the container when it exits
-  --runtime : Runtime to use for this container =nvidiaでNVIDIA製のruncを使う。
- --shm-size : Size of /dev/shm POSIXライブラリなどが利用する共有メモリ
- --ulimit : Ulimit ユーザーリソースの制限
- --ipc : IPC mode to use プロセス間通信

※ WSL2（NVIDIA Container Toolkit）の場合、--runtime=nvidia ではなく --gpus を指定する？

Start training.
```
bash scripts/train.sh

～内容の抜粋～
GPU=8
CONFIG='configs/e2e_mask_rcnn_R_50_FPN_1x.yaml'
python -m torch.distributed.launch --nproc_per_node=$GPU tools/train_net.py \
      --config-file $CONFIG \
      DTYPE "${DTYPE:-float16}" \
      NHWC "${NHWC:-True}" \
      DATALOADER.HYBRID "${HYBRID:-True}" \
      OUTPUT_DIR $RESULTS \
      | tee $LOGFILE
```
- tools/train_net.pyを起動
- configs/e2e_mask_rcnn_R_50_FPN_1x.yamlを利用
- -m mod : run library module as a script (terminates option list)・・・どういう意味？　torch.distributed.launchは分散学習（複数GPUが必要？）ののためのモジュールのよう

Start validation/evaluation.
```
bash scripts/eval.sh

～内容の抜粋～
python3 -m torch.distributed.launch --nproc_per_node=$GPU tools/test_net.py \
    --config-file $CONFIG \
    DATASETS.TEST "(\"coco_2017_val\",)" \
    DTYPE "float16" \
    OUTPUT_DIR $FOLDER \
    | tee $LOGFILE
```
- tools/test_net.pyを起動

Start inference/predictions.
```
bash scripts/inference.sh configs/e2e_mask_rcnn_R_50_FPN_1x.yaml

～内容の抜粋～
python3 -m torch.distributed.launch --nproc_per_node=$GPU tools/test_net.py \
    --config-file $CONFIG \
    --skip-eval \
    DTYPE "float16" \
    DATASETS.TEST "(\"coco_2017_val\",)" \
    OUTPUT_DIR $FOLDER \
    TEST.IMS_PER_BATCH 1 \
    | tee $LOGFILE
```

# How to train on a custom dataset.
To be investigated.

# References

- [Quick Start Guide](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Segmentation/MaskRCNN#setup)
