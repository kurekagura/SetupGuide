# はじめに

「nvcr.io/nvidia/pytorch:21.12-py3」を意識しておく。
```
#python -V
Python 3.8.12
#nvcc -V
root@1231a5133292:/workspace/object_detection# nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Mon_Sep_13_19:13:29_PDT_2021
Cuda compilation tools, release 11.5, V11.5.50
Build cuda_11.5.r11.5/compiler.30411180_0
#cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
#define CUDNN_MAJOR 8
#define CUDNN_MINOR 3
#define CUDNN_PATCHLEVEL 1

torch.__version__ => 1.11.0a0+b6df043
torch.version.cuda => 11.5
torch.backends.cudnn.version() => 8301
```
<ins>torch 1.11 CUDA 11.5 Python 3.8.12<ins>

# コード修正

- [NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Segmentation/MaskRCNN)のpytorch配下にWindowsビルドできるコード修正を施した（[別紙](./Windows%E3%83%93%E3%83%AB%E3%83%89%E5%AF%BE%E5%BF%9C.md)）

```
(...)\lib\site-packages\torch\include\pybind11\cast.h(1429):
 error: too few arguments for template template parameter "Tuple"
```
=>５つのエラーが発生する環境がある。

# 最初に結論

以下のCUDAバージョンでビルドブレークする。

|torch\cuda|11.0|11.1|11.2|11.3|11.4|11.5*|11.6|11.7|
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|1.11.0*| ○ | ○ | N/A | ○ | N/A | × | × | ○ |

NGCコンテナとTorchとCUDAバージョン(*のバージョン)を合致させる方針であったが、build/installのときのみ、「○」のバージョンを利用するしかなさそう（実行はCUDA11.5）。

# 各バージョンで試した履歴

|torch\cuda|cu11.3|cu11.4|cu11.5*|cu11.6|cu11.7|
|:---|:---:|:---:|:---:|:---:|:---:|
|1.11.0*| ○ | - | ○ NGC| | |
|1.12.0| | - | | × | |
|1.12.1| | - | | × | |
|1.13.0| | - | | × | ○ |

Start `x64 Native Tools Command Prompt for VS 2019`.
## CUDA11.3

### torch==1.11.0+cu113=>Successs!!
```
conda create --name nvmrcnn_cu113_tch1.11.0 python=3.8.12 -y
conda activate nvmrcnn_cu113_tch1.11.0

# CUDA 11.3
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113

conda install cython=0.29.32 -y
#cythonの後でないと失敗する。
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py build
```
=>Successs!!

## CUDA11.4/11.5対応の正式torch

ここには掲載なし。[INSTALLING PREVIOUS VERSIONS OF PYTORCH](https://pytorch.org/get-started/previous-versions/#installing-previous-versions-of-pytorch)

CUDA11.4は無い。
https://download.pytorch.org/whl/cu114

<ins>CUDA11.5はある。</ins>
https://download.pytorch.org/whl/cu115

## CUDA11.5

## torch==1.11.0+cu115

[torch-1.11.0+cu115-cp38-cp38-win_amd64.whl](https://download.pytorch.org/whl/cu115/torch-1.11.0%2Bcu115-cp38-cp38-win_amd64.whl)
```
conda create --name nvmrcnn_cu115_tch1.11.0 python=3.8.12 -y
conda activate nvmrcnn_cu115_tch1.11.0

#公式サイトに未掲載
pip install torch==1.11.0+cu115 torchvision==0.12.0+cu115 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu115
## CUDA 11.3（参考）
#pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
#Successfully installed charset-normalizer-2.1.1 idna-3.4 numpy-1.23.5 pillow-9.3.0 requests-2.28.1 torch-1.11.0+cu115 torchaudio-0.11.0+cu115 torchvision-0.12.0+cu115 typing-extensions-4.4.0 urllib3-1.26.13

conda install cython=0.29.32 -y
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py clean build
```
=>５つの同件エラー

【気がついた点】

<ins>このエラーはnvccのバージョンに起因している。</ins>

CUDA（nvcc）バージョンの変更して試してみた。環境変数の変更、コンソール再起動/conda activateし、以下のような状態にしてから`python setup.py build`をしてみた。

```
>where nvcc&where nvvp
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\bin\nvvp.bat
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\libnvvp\nvvp.exe
=>Successs!!
```
同じ手順で各CUDAバージョンで確認した。
```
CUDA11.0=>Successs!!
CUDA11.1=>Successs!!
CUDA11.2=>手元に無い為、未確認
CUDA11.3=>Successs!!
CUDA11.4=>手元に無い為、未確認
CUDA11.5=>５つの同件エラー
CUDA11.6=>５つの同件エラー
CUDA11.7=>Successs!!
```

## CUDA11.6

### torch==1.12.0+cu116
```
conda create --name nvmrcnn_cu116_tch1.12.0 python=3.8.12 -y
conda activate nvmrcnn_cu116_tch1.12.0

#CUDA 11.6対応で一番古いtorch1.12.0
pip install torch==1.12.0+cu116 torchvision==0.13.0+cu116 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu116
conda install cython=0.29.32 -y
#cythonの後でないと失敗する。
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py build
```
```
(...)nvmrcnn_cu116\lib\site-packages\torch\include\pybind11\cast.h(1429):
 error: too few arguments for template template parameter "Tuple"
```
=>５つの同件エラー

### torch==1.12.1+cu116
```
conda create --name nvmrcnn_cu116_tch1.12.1 python=3.8.12 -y
conda activate nvmrcnn_cu116_tch1.12.1
# CUDA 11.6
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116

conda install cython=0.29.32 -y
#cythonの後でないと失敗する。
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py build
```
=>５つの同件エラー

### torch==1.13.0+cu116
```
conda create --name nvmrcnn_cu116_tch1.13.0 python=3.8.12 -y
conda activate nvmrcnn_cu116_tch1.13.0

pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

conda install cython=0.29.32 -y
#cythonの後でないと失敗する。
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py build
```
>５つの同件エラー

「`x64 Native Tools Command Prompt for VS 2019`」でも同じエラー。

## CUDA11.7

Start 'x64 Native Tools Command Prompt for VS 2019'.

### torch==1.13.0+cu117=>Successs!!

```
conda create --name nvmrcnn_cu117_tch1.13.0 python=3.8.12 -y
conda activate nvmrcnn_cu117_tch1.13.0

pip3 install torch==1.13.0+cu117 torchvision===0.14.0+cu117 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117

#Successfully installed charset-normalizer-2.1.1 idna-3.4 numpy-1.23.5 pillow-9.3.0 requests-2.28.1 torch-1.13.0+cu117 torchaudio-0.13.0+cu117 torchvision-0.14.0+cu117 typing-extensions-4.4.0 urllib3-1.26.12

conda install cython=0.29.32 -y
#cythonとnumpyの後でないと失敗する。
pip install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"

pip install mlperf-compliance==0.0.10
pip install opencv-python==4.4.0.42
pip install yacs==0.1.8

cd O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch
set DISTUTILS_USE_SDK=1
python setup.py build
```
=>Successs!!
