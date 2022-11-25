"""
This code is based on the instructions in this URL.
https://github.com/facebookresearch/maskrcnn-benchmark#inference-in-a-few-lines
"""
import sys
#VS seems to have added it automatically.
#import os
#print(os.getcwd())
#sys.path.append(os.getcwd())
from maskrcnn_benchmark.config import cfg
from predictor import COCODemo
import cv2
import torch

print(f"sys.version => {sys.version}")
print(f"torch.__version__ => {torch.__version__}")
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print(f"torch.version.cuda => {torch.version.cuda}")
    print(f"torch.backends.cudnn.version() => {torch.backends.cudnn.version()}")

config_file = "../configs/caffe2/e2e_mask_rcnn_R_50_FPN_1x_caffe2.yaml"

# update the config options with the config file
cfg.merge_from_file(config_file)
# manual override some options
# cfg.merge_from_list(["MODEL.DEVICE", "cpu"])

coco_demo = COCODemo(
    cfg,
    min_image_size=800,
    confidence_threshold=0.7,
)
# load image and then run prediction
image = cv2.imread("./demo.jpg")
predictions = coco_demo.run_on_opencv_image(image)

cv2.imshow("predictions", predictions)
cv2.waitKey()
cv2.destroyAllWindows()
