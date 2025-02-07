# cuDNN

## CUDA v12.6

cudnn-windows-x86_64-9.7.1.26_cuda12-archive.zip

bin配下の.dllを

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin

include配下の.hを

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include

lib\x64配下の.libを

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\lib\x64

へコピーする

## 確認

cuDNN は、ヘッダーファイル名がバージョンによって異なるので注意。

cuDNN8以降：`cudnn_version.h`

```cmd
# cuDNN8以降
PS>Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\cudnn_version.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2
```

cuDNN7以前：`cudnn.h`  

```cmd
# cuDNN7以前
PS>Select-String -Path "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.?\include\cudnn.h" -Pattern "#define CUDNN_MAJOR" -Context 0,2
```
