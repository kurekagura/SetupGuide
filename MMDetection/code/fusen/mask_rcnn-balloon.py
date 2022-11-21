# このコンフィグ(code/thisfile)からの相対パス
_base_ = '../mmdetection/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
    roi_head=dict(
        bbox_head=dict(num_classes=1),
        mask_head=dict(num_classes=1)))

# 以下はWorkingDir(code)からの相対パス
dataset_type = 'COCODataset'
classes = ('balloon',)
data = dict(
    train=dict(
        img_prefix='fusen/ds/train/',
        classes=classes,
        ann_file='fusen/annot/train.json'),
    val=dict(
        img_prefix='fusen/ds/val/',
        classes=classes,
        ann_file='fusen/annot/val.json'),
    test=dict(
        img_prefix='fusen/ds/val/',
        classes=classes,
        ann_file='fusen/annot/val.json'))

load_from = 'chkp/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
