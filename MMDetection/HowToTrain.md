# [2: TRAIN WITH CUSTOMIZED DATASETS](https://mmdetection.readthedocs.io/en/latest/2_new_data_model.html#train-with-customized-datasets)

ドキュメントにはBalloonデータセットを例とした手順が記載されている。

## COCO Formatへの変換

MMDetectionのmAPの評価は、COCOフォーマットにのみ対応している為、インスタンスセグメンテーションを利用する場合、COCOフォーマットに変換する必要がある。

[matterportのリポジトリ](https://github.com/matterport/Mask_RCNN/releases)からダウンロードできる「Baloon Dataset」([balloon_dataset.zip](https://github.com/matterport/Mask_RCNN/releases/download/v2.1/balloon_dataset.zip))に同梱されているアノテーションファイルを[COCOフォーマットへ変換するPython関数が示されている。](https://mmdetection.readthedocs.io/en/latest/2_new_data_model.html#prepare-the-customized-dataset)

この関数を用いた[こちらのコード](./code/fusen/annot2coco.py)でCOCOフォーマットへ変換する。

## Configの作成

※ MMDetectionでは、約800のconfigファイルが準備されており、mask_rcnnだけでもconfigが約30ファイル提供されている。

データセットをロードできるようconfig（.py）を作成する。MaskRCNN-Balloonデータセットで作成する[`mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py`のコードが示されている。](https://mmdetection.readthedocs.io/en/latest/2_new_data_model.html#prepare-a-config)

```
～抜粋～
_base_ = 'mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py'
```
<ins>【重要】自作するconfig.pyからの相対パスで表記する。</ins>

これはさらに次に示す複数のconfigをベースとしているだった。
```
_base_ = [
    '../_base_/models/mask_rcnn_r50_fpn.py',
    '../_base_/datasets/coco_instance.py',
    '../_base_/schedules/schedule_1x.py',
    '../_base_/default_runtime.py'
]
```

```
～抜粋～
# 高速化のために事前学習済みモデルを用いる。
load_from = 'checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
```
<ins>【重要】ワーキングディレクトリからの相対パスで表記する。</ins>

## 学習

MMDetectionのtrain.pyを利用する。
```
python tools/train.py configs/balloon/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py
```
※ カスタムconfig.pyのファイル名、パスは適切に指定すること。

`work_dirs\<config名>`フォルダが作成される。その中にlog、チェックポイントファイル、最終の学習済みモデル（latest.pth）が生成される。

## テストと推論

```
python tools/test.py configs/balloon/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon.py work_dirs/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_balloon/latest.pth --eval bbox segm
```
※ カスタムconfig.py/学習済みモデル.pthのファイル名、パスは適切に指定すること。
