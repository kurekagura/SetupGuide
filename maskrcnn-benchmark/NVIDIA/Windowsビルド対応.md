# Notes

- python setup.py build の方がログが見やすい。
- 深い階層にcloneするとパスが長いという警告かエラーが出てた。
- <ins>MSVC 2019が推奨。2017はdeprecatedになるよ、という警告がでてた。</ins>

# Errors and fix

```
python setup.py build|findstr fatal

O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\ROIAlign_cuda.cu(7): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\match_proposals.cu(20): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\box_iou.cu(19): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu(7): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\ROIPool_cuda.cu(7): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\box_encode.cu(19): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\generate_mask_targets.cu(24): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\rpn_generate_proposals.cu(21): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda/rpn_generate_proposals.h(20): fatal error C1083: include ファイルを開けません。'THC/THC.h':No such file or directory
```
[Replacing THC/THC.h module to ATen/ATen.h module](https://stackoverflow.com/questions/72988735/replacing-thc-thc-h-module-to-aten-aten-h-module)

```
● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\ROIAlign_cuda.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\match_proposals.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\box_iou.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\ROIPool_cuda.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\box_encode.cu

● O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\generate_mask_targets.cu

● 
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\rpn_generate_proposals.cu

O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda/rpn_generate_proposals.h
```

```
[1/7] C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.5\bin\nvcc --generate-dependencies-with-compile --dependency-output O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu(84): error: identifier "THCState" is undefined

O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu(84): error: identifier "state" is undefined

O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu(90): error: name followed by "::" must be a class or namespace name

O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu(126): error: name followed by "::" must be a class or namespace name

4 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/nms.cu".
```
後続で利用されていない変数と初期化行をコメントアウト（初期化に問題が生じないか？）
```
THCState *state = at::globalContext().lazyInitCUDA(); // TODO replace with getTHCState
```
```
[1/7] 
(...)
O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\ROIPool_cuda.cu(130): error: no instance of function template "at::ceil_div" matches the argument list
            argument types are: (long long, long)
```
longの利用はダメ。long longもしくはint64_tを用いるように修正。
```
- ROIPool_cuda.cu
//auto output_size = num_rois * pooled_height * pooled_width * channels;
↓
int64_t output_size = num_rois * pooled_height * pooled_width * channels;

//dim3 grid(std::min(at::ceil_div(output_size, 512L), 4096L));
↓
dim3 grid(std::min(at::ceil_div(output_size, 512LL), 4096LL));

//dim3 grid(std::min(at::ceil_div(grad.numel(), 512L), 4096L));
↓
dim3 grid(std::min(at::ceil_div(grad.numel(), 512LL), 4096LL));
```

```
(...)\maskrcnn_benchmark\csrc\cuda\nms.cu(90): error: 
name followed by "::" must be a class or namespace name

(...)\maskrcnn_benchmark\csrc\cuda\nms.cu(126): error: 
name followed by "::" must be a class or namespace name
```
以下の二か所でエラーが発生している。
```
- nms.cu
mask_dev = 
(unsigned long long*)c10::cuda::CUDACachingAllocator::raw_alloc(boxes_num * col_blocks * sizeof(unsigned long long));

c10::cuda::CUDACachingAllocator::raw_delete(mask_dev);
```
CUDACachingAllocator.hをincludeする。
```
#include <c10/cuda/CUDACachingAllocator.h>
```

```
FAILED: (...) O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\match_proposals.cu -o (...)o:\sw\Anaconda3\envs\nvmrcnn_cu115\lib\site-packages\torch\include\pybind11\cast.h(1429): error: too few arguments for template template parameter "Tuple"
          detected during instantiation of class "pybind11::detail::tuple_caster<Tuple, Ts...> [with Tuple=std::pair, Ts=<T1, T2>]" 
(1507): here

o:\sw\Anaconda3\envs\nvmrcnn_cu115\lib\site-packages\torch\include\pybind11\cast.h(1503): error: too few arguments for template template parameter "Tuple"
          detected during instantiation of class "pybind11::detail::tuple_caster<Tuple, Ts...> [with Tuple=std::pair, Ts=<T1, T2>]" 
(1507): here

2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/match_proposals.cu".
```

[1/6～5/6]は同件。
```
[1/6] 
2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/match_proposals.cu".
match_proposals.cu
[2/6]
2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/box_iou.cu".
box_iou.cu
[3/6]
2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/generate_mask_targets.cu".
generate_mask_targets.cu
[4/6]
2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/box_encode.cu".
box_encode.cu
[5/6]
2 errors detected in the compilation of "O:/src/NVIDIA/DeepLearningExamples/PyTorch/Segmentation/MaskRCNN/pytorch/maskrcnn_benchmark/csrc/cuda/rpn_generate_proposals.cu".
rpn_generate_proposals.cu
[6/6]
-c O:\src\NVIDIA\DeepLearningExamples\PyTorch\Segmentation\MaskRCNN\pytorch\maskrcnn_benchmark\csrc\cuda\nms.cu
```

[error: too few arguments for template template parameter "Tuple" detected during instantiation of class "pybind11::detail::tuple_caster<Tuple, Ts...> #1024](https://github.com/facebookresearch/pytorch3d/issues/1024)

エラー確認(VS2019)
- torch 1.11.0+cu115

<ins>torch 1.13.0+cu117⇒上記エラー解決！別のエラー（error LNK2001: 外部シンボルxxは未解決です）だけになる。</link>

VS2017/VS2019でも同じ。

```
python setup.py build 2>&1 |findstr LNK2001

●match_proposals.obj : error LNK2001: 外部シンボル "public: long * __cdecl at::TensorBase::data_ptr<long>(void)const " (??$data_ptr@J@TensorBase@at@@QEBAPEAJXZ) は未解決です

●rpn_generate_proposals.obj : error LNK2001: 外部シンボル "public: long * __cdecl at::TensorBase::data_ptr<long>(void)const " (??$data_ptr@J@TensorBase@at@@QEBAPEAJXZ) は未解決です

●vision.obj : error LNK2001: 外部シンボル GeneratePreNMSUprightBoxes は未解決です
```

rpn_generate_proposals.h/rpn_generate_proposals.cu
```
- rpn_generate_proposals.h
//std::vector<at::Tensor> GeneratePreNMSUprightBoxes(
↓
extern "C" __declspec(dllexport) std::vector<at::Tensor> GeneratePreNMSUprightBoxes(

- rpn_generate_proposals.cu
//std::vector<at::Tensor> GeneratePreNMSUprightBoxes(
↓
extern "C" __declspec(dllexport) std::vector<at::Tensor> GeneratePreNMSUprightBoxes(
```
vision.obj : error LNK2001が解決。

[Strange link error seen by multiple people while building PyTorch cpp/cuda extensions](https://forums.developer.nvidia.com/t/strange-link-error-seen-by-multiple-people-while-building-pytorch-cpp-cuda-extensions/145261)

```
- rpn_generate_proposals.cu
//const long *d_sorted_scores_keys,
↓
const int64_t *d_sorted_scores_keys, 

//sorted_indices.data_ptr<long>(),
↓
sorted_indices.data_ptr<int64_t>(),
```
rpn_generate_proposals.obj : error LNK2001が解決。

```
- match_proposals.cu
//void max_along_gt_idx(float *match, unsigned char *pred_forgiven, long *max_gt_idx, long long gt,long long preds,
//  bool include_low_quality, float low_th, float high_th) {
↓
void max_along_gt_idx(float *match, unsigned char *pred_forgiven, int64_t *max_gt_idx, long long gt,long long preds,
    bool include_low_quality, float low_th, float high_th) {

//result.data_ptr<long>(), 
↓
result.data_ptr<int64_t>(),
```

以上の修正で、`python setup.py build`はパスするようになり、`pip install -v -e .`も成功した。

「x64 Native Tools Command Prompt for VS 2019」を利用
```
conda list|findstr "torch torchvision cython maskrcnn-benchmark"
cython                    0.29.32          py38hd77b12b_0
maskrcnn-benchmark        0.1                       dev_0    <develop>
torch                     1.13.0+cu117             pypi_0    pypi
torchaudio                0.13.0+cu117             pypi_0    pypi
torchvision               0.14.0+cu117             pypi_0    pypi
```