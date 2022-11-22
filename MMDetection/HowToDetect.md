# How to detect.

>cd mmdetection

[YOLOv3](https://github.com/open-mmlab/mmdetection/tree/master/configs/yolo)
```
mim download mmdet --config yolov3_mobilenetv2_mstrain-416_300e_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/yolov3_mobilenetv2_mstrain-416_300e_coco.py ../chkp/yolov3_mobilenetv2_mstrain-416_300e_coco_20210718_010823-f68a07b3.pth --device cuda
````
```
mim download mmdet --config yolov3_d53_320_273e_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/yolov3_d53_320_273e_coco.py ../chkp/yolov3_d53_320_273e_coco-421362b6.pth --device cuda
```

[Faster R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn)
```
mim download mmdet --config faster_rcnn_r50_fpn_1x_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/faster_rcnn_r50_fpn_1x_coco.py ../chkp/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth --device cuda
```

[Mask R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/mask_rcnn)
```
mim download mmdet --config mask_rcnn_r50_fpn_1x_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/mask_rcnn_r50_fpn_1x_coco.py ../chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth --device cuda
```
```
mim download mmdet --config mask_rcnn_r50_caffe_fpn_1x_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/mask_rcnn_r50_caffe_fpn_1x_coco.py ../chkp/mask_rcnn_r50_caffe_fpn_1x_coco_bbox_mAP-0.38__segm_mAP-0.344_20200504_231812-0ebd1859.pth --device cuda
```
```
mim download mmdet --config mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco --dest ../chkp
```
```
python demo/image_demo.py demo/demo.jpg ../chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py ../chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth --device cuda
```
```
mim download mmdet --config mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco --dest ../chkp
=>Error!
```
[チュートリアルで作成するmask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py](https://mmdetection.readthedocs.io/en/latest/2_new_data_model.html#prepare-the-customized-dataset)のベースとしているconfigファイルを指定してmimダウンロードするとエラーになる。
ただし、load_fromに指定されている事前学習済みのモデルは、一つ上のmimダウンロードできる。
```
# The new config inherits a base config to highlight the necessary modification
_base_ = 'mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py'
# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = 'checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
```
リポジトリから直接取得する。このconfigに直接対応した事前学習済みモデルは配布されていない（？）。
```
Invoke-WebRequest `
https://raw.githubusercontent.com/open-mmlab/mmdetection/master/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py `
-O ../chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py

python demo/image_demo.py demo/demo.jpg ../chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py ../chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth --device cuda
```

# Reference

- [Verify the installation](https://mmdetection.readthedocs.io/en/stable/get_started.html#verify-the-installation)
