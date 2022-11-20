# [Test existing models on standard datasets](https://mmdetection.readthedocs.io/en/stable/1_exist_data_model.html#test-existing-models-on-standard-datasets)

## Preparation
Check out the source from git to the "mmdetection" folder. Since there is a case where you want to delete the mmdetection folder, do not put anything other than the check-out file under the mmdetection / folder.

```
mmdetection
├── data
│   ├── coco
│   │   ├── annotations
│   │   ├── train2017
│   │   ├── val2017
│   │   ├── test2017
```
Create a junction with the above structure.
```
# In mmdetection
mkdir data && cd data
# Run as administrator
mklink /J coco o:\datasets\coco2017
```

Download Config (.py) and the checkpoint pre-trained model (.pth). The mim command downloads both config.py and .pth files to the specified folder, but config.py can also be checked out from GitHub, so you can use configs/xxx/xxx.py.

In `mmdetection/`.
```
mim download mmdet --config yolov3_mobilenetv2_mstrain-416_300e_coco --dest ../chkp
mim download mmdet --config faster_rcnn_r50_fpn_1x_coco --dest ../chkp
mim download mmdet --config mask_rcnn_r50_fpn_1x_coco --dest ../chkp

```

## Practice
Command submission in PowerShell.

* Test Yolov3 MobileNetV2.
```
python tools/test.py `
configs/yolo/yolov3_mobilenetv2_mstrain-416_300e_coco.py `
../chkp/yolov3_mobilenetv2_mstrain-416_300e_coco_20210718_010823-f68a07b3.pth `
--out result-yolov3_mobilenetv2_mstrain-416_300e_coco.pkl `
--eval bbox
```
* Test Faster R-CNN 
```
python tools/test.py `
configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py `
../chkp/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth `
--out result-faster_rcnn_r50_fpn_1x_coco.pkl `
--eval bbox segm
```
* Test Mask R-CNN
```
python tools/test.py `
configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py `
../chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth `
--out result-mask_rcnn_r50_fpn_1x_coco.pkl `
--eval bbox segm
```
e.g.)
```
(...)UserWarning: 
Setting OMP_NUM_THREADS environment variable for each process to be 1 in default,
to avoid your system being overloaded,
please further tune the variable for optimal performance in your application as needed.
(...)UserWarning: 
Setting MKL_NUM_THREADS environment variable for each process to be 1 in default,
to avoid your system being overloaded,
please further tune the variable for optimal performance in your application as needed.
(...)
loading annotations into memory...
Done (t=0.57s)
creating index...
index created!
load checkpoint from local path: ../chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth
[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>] 5000/5000, 
11.3 task/s, elapsed: 442s, ETA:     0s
writing results to result-mask_rcnn_r50_fpn_1x_coco.pkl

Evaluating bbox...
Loading and preparing results...
DONE (t=0.33s)
creating index...
index created!
Running per image evaluation...
Evaluate annotation type *bbox*
DONE (t=20.39s).
Accumulating evaluation results...
DONE (t=4.36s).

 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.382
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=1000 ] = 0.588
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=1000 ] = 0.414
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.219
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.409
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.495
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.524
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.524
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=1000 ] = 0.524
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.329
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.557
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.662

Evaluating segm...
(...)mmdetection\mmdet\datasets\coco.py:474:UserWarning:
The key "bbox" is deleted for more accurate mask AP of small/medium/large instances since v2.12.0. 
This does not change the overall mAP calculation.

Loading and preparing results...
DONE (t=1.22s)
creating index...
index created!
Running per image evaluation...
Evaluate annotation type *segm*
DONE (t=23.22s).
Accumulating evaluation results...
DONE (t=4.28s).

 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.347
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=1000 ] = 0.557
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=1000 ] = 0.372
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.158
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.369
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.511
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.478
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.478
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=1000 ] = 0.478
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=1000 ] = 0.280
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=1000 ] = 0.514
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=1000 ] = 0.626

OrderedDict([
    ('bbox_mAP', 0.382), 
    ('bbox_mAP_50', 0.588), 
    ('bbox_mAP_75', 0.414), 
    ('bbox_mAP_s', 0.219), 
    ('bbox_mAP_m', 0.409), 
    ('bbox_mAP_l', 0.495), 
    ('bbox_mAP_copypaste', '0.382 0.588 0.414 0.219 0.409 0.495'), 
    ('segm_mAP', 0.347), 
    ('segm_mAP_50', 0.557), 
    ('segm_mAP_75', 0.372), 
    ('segm_mAP_s', 0.158), 
    ('segm_mAP_m', 0.369), 
    ('segm_mAP_l', 0.511), 
    ('segm_mAP_copypaste', '0.347 0.557 0.372 0.158 0.369 0.511')])
```
