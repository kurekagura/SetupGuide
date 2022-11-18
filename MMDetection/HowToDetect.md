# How to detect.

>cd mmdetection

[YOLOv3](https://github.com/open-mmlab/mmdetection/tree/master/configs/yolo)
```
mim download mmdet --config yolov3_d53_320_273e_coco --dest ../chkp

python demo/image_demo.py demo/demo.jpg ../chkp/yolov3_d53_320_273e_coco.py ../chkp/yolov3_d53_320_273e_coco-421362b6.pth --device cuda
```

[Faster R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/faster_rcnn)
```
mim download mmdet --config faster_rcnn_r50_fpn_1x_coco --dest ../chkp

python demo/image_demo.py demo/demo.jpg ../chkp/faster_rcnn_r50_fpn_1x_coco.py ../chkp/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth --device cuda
```

[Mask R-CNN](https://github.com/open-mmlab/mmdetection/tree/master/configs/mask_rcnn)
```
mim download mmdet --config mask_rcnn_r50_fpn_1x_coco --dest ../chkp

python demo/image_demo.py demo/demo.jpg ../chkp/mask_rcnn_r50_fpn_1x_coco.py ../chkp/mask_rcnn_r50_fpn_1x_coco_20200205-d4b0c5d6.pth --device cuda
```


# Reference

- [Verify the installation](https://mmdetection.readthedocs.io/en/stable/get_started.html#verify-the-installation)
