# Directory structure
```
code
├── chkp
├── fusen
│   ├── mask_rcnn-balloon.py
│   ├── annot <JUNCTION>[e.g, annot-v1.1]
│   ├── annot-v1.1
│   ├── ds <JUNCTION>[e.g, o:\datasets\baloon-v1]
├── mmdetection
│   ├── configs
│   ├── tools
├── work_dirs *train.pyにより作成
```

# Train
cd into 'code'.
```
python mmdetection/tools/train.py fusen/mask_rcnn-balloon.py
```
dropped:
```
work_dirs/
    xxx.log
    epoch_1.pth
    ...
    epoch_n.pth
    mask_rcnn-balloon/latest.pth
```
# Test
test.pyでは画像の場所は指定できない（学習時の検証で利用した画像を使う）。

cd into 'code'.
```
python mmdetection/tools/test.py fusen/mask_rcnn-balloon.py work_dirs/mask_rcnn-balloon/latest.pth --eval bbox segm
```
画像ファイル毎にウィンドウを起動（'q'でウィンドウを閉じる。ctl+Cでプログラムを停止する）
```
python mmdetection/tools/test.py fusen/mask_rcnn-balloon.py work_dirs/mask_rcnn-balloon/latest.pth --show
```

# Try with any image file.
image_demo.pyは任意の画像を指定できる。
cd into 'code'.
```
python mmdetection/demo/image_demo.py fusen/imgs/test1.jpg fusen/mask_rcnn-balloon.py work_dirs/mask_rcnn-balloon/latest.pth --device cuda
```
