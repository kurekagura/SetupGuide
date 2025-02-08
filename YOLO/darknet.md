# AlexeyAB/darknet(Yolo v4, v3 and v2)

## 2025/2/8-2 CUDA12.8

- cuda_12.8.0_571.96_windows.exe
- cudnn-windows-x86_64-9.7.1.26_cuda12-archive.zip
- opencv-4.10.0-windows.exe

※　記載のない点は、2025/2/8-1と同様

`Developer Command Prompt for VS 2022`を利用

```cmd
>where cl

C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC\14.42.34433\bin\Hostx64\x64\cl.exe
```

```cmd
>where nvcc.exe && where nvvp.exe && nvcc -V

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\libnvvp\nvvp.exe
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Jan_15_19:38:46_Pacific_Standard_Time_2025
Cuda compilation tools, release 12.8, V12.8.61
Build cuda_12.8.r12.8/compiler.35404655_0
```

```PowerShell
PS> Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2

> C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\include\cudnn_version.h:57:#define CUDNN_MAJOR 9
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\include\cudnn_version.h:58:#define CUDNN_MINOR 7
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\include\cudnn_version.h:59:#define CUDNN_PATCHLEVEL 1
```

```cmd
>where cublas64_12.dll cudart64_12.dll

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin\cublas64_12.dll
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin\cudart64_12.dll
```

C:\lib\opencv-4.10.0

```cmd
>set OPENCV_DIR=C:\lib\opencv-4.10.0\build
>cmake-gui
```

## 2025/2/8-1 CUDA12.6

- cmake-3.31.5-windows-x86_64.msi

`x64 Native Tools Command Prompt for VS 2022`を利用

```cmd
>where cl
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe
```

```cmd
>where cmake && cmake --version
O:\sw\CMake\bin\cmake.exe
C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe
cmake version 3.31.5

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

```cmd
>where nvcc.exe && where nvvp.exe && nvcc -V

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\libnvvp\nvvp.exe
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Thu_Sep_12_02:55:00_Pacific_Daylight_Time_2024
Cuda compilation tools, release 12.6, V12.6.77
Build cuda_12.6.r12.6/compiler.34841621_0
```

```PowerShell
PS> Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2

> C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\cudnn_version.h:57:#define CUDNN_MAJOR 9
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\cudnn_version.h:58:#define CUDNN_MINOR 7
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\cudnn_version.h:59:#define CUDNN_PATCHLEVEL 1
```

```cmd
where cublas64_12.dll cudart64_12.dll
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\cublas64_12.dll
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\cudart64_12.dll
```

```cmd
mkdir AlexeyAB && cd AlexeyAB
git clone https://github.com/AlexeyAB/darknet.git && cd darknet
```

```cmd
>set OPENCV_DIR=O:\lib\opencv-4.10.0\build
>cmake-gui
```

CUDA複数バージョンが存在すると意図しないCUDAコンパイラが検出される（？ 当初v11.7で試したが、どうしてもv12.6が検出されてしまし、cuDNNの依存も意図したものにできなかったため、CUDAv12.6/cuDNN9.7.1とした。

CMAKE_CUDA_COMPILERを書き換えてConfigureしても、書き換え前と後の２つのCUDAバージョンがcxprojに出力されてしまい上手く行かなかった。

Releaseフォルダ配下の生成物と以下をトップにコピー

- opencv_world4100.dll
- pthreadVC2.dll

```cmd
darknet.exe detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -thresh 0.25
darknet.exe detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights
```

## 学習済みモデル

<https://github.com/AlexeyAB/darknet#pre-trained-models>

## 参考

- [AlexeyAB Darknet YOLO V4をWindowsへインストール](https://www.miki-ie.com/machinelearning/darknet-yolo-v4-windows/)

  cuda_11.3.0, opencv4.3.2
