# Reference

[mainly]

- [open-mmlab/mmdetection](https://github.com/open-mmlab/mmdetection)
- [MMDetection Doc](https://mmdetection.readthedocs.io/en/stable/get_started.html)

> MMDetection works on Linux, Windows and macOS. It requires Python 3.6+, CUDA 9.2+ and PyTorch 1.5+.

- [Compatibility issue between MMCV and MMDetection](https://mmdetection.readthedocs.io/en/stable/faq.html)

  ```text
  master mmcv-full>=1.3.17, \<1.6.0
  2.25.1 mmcv-full>=1.3.17, \<1.6.0
  2.23.0 mmcv-full>=1.3.17, \<1.5.0 ←cuda117では動作不可を確認済 
  2.24.0 mmcv-full>=1.3.17, \<1.6.0 ←Target1
  2.26.0 mmcv-full>=1.3.17, \<1.8.0 ←Target2
  ```

[Revsion]

```cmd
mmdetection>git checkout tags/v2.24.0

mmdetection>git log -n 1
commit 1376e77e6ecbaad609f6003725158de24ed42e84 (HEAD, tag: v2.24.0)
Merge: c72bc707 7d1c0970
Author: Wenwei Zhang <40779233+ZwwWayne@users.noreply.github.com>
Date:   Tue Apr 26 21:14:55 2022 +0800

↓ Updated to v2.24.1

commit 73b4e65a6a30435ef6a35f405e3474a4d9cfb234 (HEAD, tag: v2.24.1)
Author: Wenwei Zhang <40779233+ZwwWayne@users.noreply.github.com>
Date:   Sat Apr 30 22:23:14 2022 +0800

↓ Updated to v2.26.0

commit 31c84958f54287a8be2b99cbf87a6dcf12e57753 (HEAD, tag: v2.26.0, origin/master, origin/HEAD, master)
Author: Yue Zhou <592267829@qq.com>
Date:   Wed Nov 23 22:23:53 2022 +0800
```

# Environment

```text
>systeminfo |findstr /B /C:"OS Name" /B /C:"OS"
OS 名:                  Microsoft Windows 10 Pro
OS バージョン:          10.0.19045 N/A ビルド 19045

>ver
Microsoft Windows [Version 10.0.19045.2251]

>conda -V
conda 22.9.0
```

```cmd
>where nvcc && where nvvp
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin\nvvp.bat
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\libnvvp\nvvp.exe
```

```cmd
>nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Jun__8_16:59:34_Pacific_Daylight_Time_2022
Cuda compilation tools, release 11.7, V11.7.99
Build cuda_11.7.r11.7/compiler.31442593_0
```

```cmd
PS>Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2
> (omit)#define CUDNN_MAJOR 8
  (omit)#define CUDNN_MINOR 4
  (omit)#define CUDNN_PATCHLEVEL 1
```

# GPU Version Setup (manually)

Start 'x64 Native Tools Command Prompt for VS 2017'.

```cmd
conda create --name MMDetection2.24cu117 python=3.7.15 -y
conda activate MMDetection2.24cu117

#1.13.0(stable) with specified versions.
conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 blas==1.0 -c pytorch -c nvidia -y

pip install opencv-python==4.6.0.66

pip install openmim==0.3.2

#memo 2.24.0 mmcv-full>=1.3.17, \<1.6.0
#set DISTUTILS_USE_SDK=1
pip install mmcv-full==1.6.0
```

Export conda yml

```cmd
conda env export -n MMDetection2.24cu117 > conda_MMDetection2.24+cu117.yml

#Edit
#  - blas=1.0=mkl
#to
#  - defaults::blas=1.0=mkl
```

# Install MMDetection.

```cmd
# cd <base_dir>
mkdir open-mmlab && cd open-mmlab
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
git checkout tags/v2.26.0
pip install -v -e .
```

>Successfully installed contourpy-1.0.6 cycler-0.11.0 fonttools-4.38.0 kiwisolver-1.4.4 matplotlib-3.6.2 mmdet-2.26.0 pycocotools-2.0.6 scipy-1.9.3 terminaltables-3.1.10

# GPU Version Setup (use conda YAML)
Start 'x64 Native Tools Command Prompt for VS 2017'.
```
conda env create –f conda_MMDetection2.24+cu117.yml --name MMDetection2.24cu117YML
```

# Verify the installation

```cmd
# At mmdetection on conda
mim download mmdet --config mask_rcnn_r50_fpn_1x_coco --dest ./chkp

# MASK R-CNN ON CPU ON GPU
python demo/image_demo.py --device cpu demo/demo.jpg chkp/mask_rcnn_r50_fpn_1x_coco.py chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth
python demo/image_demo.py --device cuda:0 demo/demo.jpg chkp/mask_rcnn_r50_fpn_1x_coco.py chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth
```

# Verify the installation by trainnig.

## [Test existing models on standard datasets](https://mmdetection.readthedocs.io/en/stable/1_exist_data_model.html#test-existing-models-on-standard-datasets)

```
PS>python tools/test.py chkp/mask_rcnn_r50_fpn_1x_coco.py `
chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth `
--out result-mask_rcnn.pkl `
--eval bbox segm
```
git checkout tags/v2.24.0
```
Traceback (most recent call last):
  File "tools/test.py", line 16, in <module>
    from mmdet.apis import multi_gpu_test, single_gpu_test
  File "o:\src\open-mmlab\mmdetection\mmdet\__init__.py", line 26, in <module>
    f'MMCV=={mmcv.__version__} is used but incompatible. ' \
AssertionError: MMCV==1.6.0 is used but incompatible. Please install mmcv>=1.3.17, <=1.5.0.
```
git checkout tags/v2.24.1

=> Resolved.

# pip3 install torch
Start 'x64 Native Tools Command Prompt for VS 2017'.
```
conda create --name MMDetection2.24cu117pip python=3.7.15 -y
conda activate MMDetection2.24cu117pip

#1.13.0(stable) with specified versions.
#conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 blas==1.0 -c pytorch -c nvidia -y
pip3 install torch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117

pip install opencv-python==4.6.0.66

pip install openmim==0.3.2

#memo 2.24.0 mmcv-full>=1.3.17, \<1.6.0
pip install mmcv-full==1.6.0
```
```
conda env export -n MMDetection2.24cu117pip > conda_MMDetection2.24+cu117pip.yml
```
Inserted this.
```
  - pip:
    - --extra-index-url https://download.pytorch.org/whl/cu117
    (...)
```
```
conda env create –f conda_MMDetection2.24+cu117pip.yml -n MMDetection2.24cu117pipYML
```

# memo
```
conda list |findstr "pytorch torchvision torchaudio pytorch-cuda blas"
```
```
#1.13.0(stable)
#Official Command
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

#specified version for the future.
conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 blas==1.0 -c pytorch -c nvidia

blas                      1.0                         mkl
libcublas                 11.11.3.6                     0    nvidia
libcublas-dev             11.11.3.6                     0    nvidia
pytorch                   1.13.0          py3.7_cuda11.7_cudnn8_0    pytorch
pytorch-cuda              11.7                 h67b0de4_0    pytorch
pytorch-mutex             1.0                        cuda    pytorch
torchaudio                0.13.0                   pypi_0    pypi
torchvision               0.14.0                   pypi_0    pypi
```

```
conda uninstall pytorch torchvision torchaudio pytorch-cuda
```

```
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```
