# Environment

```
>systeminfo |findstr /B /C:"OS Name" /B /C:"OS"
OS 名:                  Microsoft Windows 10 Pro
OS バージョン:          10.0.19045 N/A ビルド 19045

>ver
Microsoft Windows [Version 10.0.19045.2251]

>wsl --list --verbose
  NAME                   STATE           VERSION
* Ubuntu-22.04           Stopped         2
  docker-desktop         Stopped         2
  docker-desktop-data    Stopped         2
>wsl --status
既定の配布: Ubuntu-22.04
既定のバージョン: 2
Linux 用 Windows サブシステムの最終更新日: 2022/08/02
WSL の自動更新が有効になっています。
カーネル バージョン: 5.10.102.1
```
```
> docker version
Client:
 Cloud integration: v1.0.28
 Version:           20.10.17
 API version:       1.41
 Go version:        go1.17.11
 Git commit:        100c701
 Built:             Mon Jun  6 23:09:02 2022
 OS/Arch:           windows/amd64
 Context:           default
 Experimental:      true

Server: Docker Desktop 4.11.0 (83626)
 Engine:
  Version:          20.10.17
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.17.11
  Git commit:       a89b842
  Built:            Mon Jun  6 23:01:23 2022
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.6
  GitCommit:        10c12954828e7c7c9b6e0ea9b0c02b01407d3ae1
 runc:
  Version:          1.1.2
  GitCommit:        v1.1.2-0-ga916309
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```
```
>where nvcc && where nvvp
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\bin\nvvp.bat
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\libnvvp\nvvp.exe
```
```
>nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Thu_Nov_18_09:52:33_Pacific_Standard_Time_2021
Cuda compilation tools, release 11.5, V11.5.119
Build cuda_11.5.r11.5/compiler.30672275_0
```
```
PS>Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2
> (...)\cudnn_version.h:57:#define CUDNN_MAJOR 8
  (...)cudnn_version.h:58:#define CUDNN_MINOR 3
  (...)\cudnn_version.h:59:#define CUDNN_PATCHLEVEL 3
```
# How to run
Start PS(or cmd)
```
docker run --gpus all -it --rm nvcr.io/nvidia/pytorch:21.12-py3 /bin/bash
```
In this container.
```
# nvidia-smi
Wed Nov 16 12:15:13 2022
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.46       Driver Version: 526.47       CUDA Version: 12.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
```
If the GPU is not detected, the nvidia-sim responses "bash: nvidia-sim: command not found".

# Try other container image

[Mask R-CNN For PyTorch](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Segmentation/MaskRCNN)

Start pwsh.
```
cd <your_base_dir>
mkdir NVIDIA && cd NVIDIA
git clone https://github.com/NVIDIA/DeepLearningExamples.git
cd .\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\
docker build --rm -t nvidia_joc_maskrcnn_pt . -f Dockerfile
```

```
docker run `
    -v ""O:/coco/coco2017"":""/datasets/data"" `
    --gpus all `
    --rm --name=mymaskrccbench `
    --shm-size=2g `
    --ulimit memlock=-1 --ulimit stack=8388608 `
    --ipc=host `
    -it nvidia_joc_maskrcnn_pt /bin/bash
```
memo:
- --ulimit stack=(kbytes) 64G=>67108864 8G=>8388608
- --runtime=nvidia causes an error(Unknown runtime specified nvidia.). so specify --gpus all.
- From pwsh
  ```
  -v "O:/coco/coco2017":"/datasets/data" ->Error
  -v ""O:/coco/coco2017"":""/datasets/data"" ->OK
  ```

```
wget https://raw.githubusercontent.com/kurekagura/SetupGuide/main/CUDA/check-cuda-torch.py .
python check-cuda-torch.py
```

# WSL Tips
```
#使用可能な Linux ディストリビューションを一覧表示(-l -o)
wsl --list --online
#インストールされている Linux ディストリビューションを一覧表示(-l -v)
wsl --list --verbose
#WSL の状態を確認する
wsl --status
```
