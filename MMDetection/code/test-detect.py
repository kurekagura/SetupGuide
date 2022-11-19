from mmdet.apis import init_detector, inference_detector,show_result_pyplot
import mmcv

config_file = './chkp/yolov3_mobilenetv2_mstrain-416_300e_coco.py'
checkpoint_file = './chkp/yolov3_mobilenetv2_mstrain-416_300e_coco_20210718_010823-f68a07b3.pth'

model = init_detector(config_file, checkpoint_file, device='cuda')

img = './mmdetection/demo/demo.jpg'
img = mmcv.imread(img)
result = inference_detector(model, img) #which will only load it once

#VS/vscodeからウィンドウが出ない。
#model.show_result(img, result)
show_result_pyplot(model, img, result)