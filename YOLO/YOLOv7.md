# YOLOv7

## CUDA11.7

`x64 Native Tools Command Prompt for VS 2022`を利用

```cmd
>where cl
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe
```

```cmd
>where nvcc.exe && where nvvp.exe && nvcc -V

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\bin\nvcc.exe
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\libnvvp\nvvp.exe
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Jun__8_16:59:34_Pacific_Daylight_Time_2022
Cuda compilation tools, release 11.7, V11.7.99
Build cuda_11.7.r11.7/compiler.31442593_0
```

```PowerShell
PS> Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2

> C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include\cudnn_version.h:57:#define CUDNN_MAJOR 8
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include\cudnn_version.h:58:#define CUDNN_MINOR 4
  C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include\cudnn_version.h:59:#define CUDNN_PATCHLEVEL 1
```

```cmd
mkdir WongKinYiu && cd WongKinYiu
git clone --recursive https://github.com/WongKinYiu/yolov7
cd yolov7
```

```cmd
py -3.10 -m venv .py310
.py310\Scripts\activate.bat
```

```console
python.exe -m pip install -U pip setuptools wheel
pip install -U cython
pip install cython_bbox
pip install --no-cache-dir "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
```

※pycocotoolsでビルドエラーがでる場合、pip/setuptools/wheelのアップグレードかcython_bboxのインストールを試す。

```cmd
pip install -r requirements.txt
```

```cmd
# CUDA 11.7
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2
```

```cmd
>pip list
Package                 Version
----------------------- --------------------
absl-py                 2.1.0
asttokens               3.0.0
certifi                 2025.1.31
charset-normalizer      3.4.1
colorama                0.4.6
contourpy               1.3.1
cycler                  0.12.1
Cython                  3.0.11
cython_bbox             0.1.5
decorator               5.1.1
exceptiongroup          1.2.2
executing               2.2.0
filelock                3.17.0
fonttools               4.55.8
fsspec                  2025.2.0
grpcio                  1.70.0
idna                    3.10
ipython                 8.32.0
jedi                    0.19.2
Jinja2                  3.1.5
kiwisolver              1.4.8
Markdown                3.7
MarkupSafe              3.0.2
matplotlib              3.10.0
matplotlib-inline       0.1.7
mpmath                  1.3.0
networkx                3.4.2
numpy                   1.23.5
opencv-python           4.11.0.86
packaging               24.2
pandas                  2.2.3
parso                   0.8.4
pillow                  11.1.0
pip                     25.0
prompt_toolkit          3.0.50
protobuf                4.21.2
psutil                  6.1.1
pure_eval               0.2.3
pycocotools             2.0
Pygments                2.19.1
pyparsing               3.2.1
python-dateutil         2.9.0.post0
pytz                    2025.1
PyYAML                  6.0.2
requests                2.32.3
scipy                   1.15.1
seaborn                 0.13.2
setuptools              75.8.0
six                     1.17.0
stack-data              0.6.3
sympy                   1.13.1
tensorboard             2.18.0
tensorboard-data-server 0.7.2
thop                    0.1.1.post2209072238
torch                   2.0.1
torchaudio              2.0.2
torchvision             0.15.2
tqdm                    4.67.1
traitlets               5.14.3
typing_extensions       4.12.2
tzdata                  2025.1
urllib3                 2.3.0
wcwidth                 0.2.13
Werkzeug                3.1.3
wheel                   0.45.1
```

```cmd
url -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7x.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-e6.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-d6.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-e6e.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6-pose.pt
curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-mask.pt
```

```cmd
pip list
Package     Version
----------- -------
Cython      3.0.11
cython_bbox 0.1.5
numpy       2.2.2
pip         25.0
pycocotools 2.0
setuptools  75.8.0
wheel       0.45.1
```

```cmd
python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source inference/images/horses.jpg
```

runs\detect\exp10\horses.jpg に推論結果が出力される

## CUDA11.8(11.xの最新)

## 参考

[物体検出，姿勢推定の実行（YOLOv7，PyTorch，Python を使用）（Windows 上）](https://www.kkaneko.jp/ai/win/yolov7.html)
