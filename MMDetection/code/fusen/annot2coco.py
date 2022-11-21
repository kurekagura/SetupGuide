"""
https://mmdetection.readthedocs.io/en/latest/2_new_data_model.html#prepare-the-customized-dataset
"""
import os
import os.path as osp
import mmcv

def convert_balloon_to_coco(ann_file, out_file, image_prefix):
    data_infos = mmcv.load(ann_file)

    annotations = []
    images = []
    obj_count = 0
    for idx, v in enumerate(mmcv.track_iter_progress(data_infos.values())):
        filename = v['filename']
        img_path = osp.join(image_prefix, filename)
        height, width = mmcv.imread(img_path).shape[:2]

        images.append(dict(
            id=idx,
            file_name=filename,
            height=height,
            width=width))

        bboxes = []
        labels = []
        masks = []
        for _, obj in v['regions'].items():
            assert not obj['region_attributes']
            obj = obj['shape_attributes']
            px = obj['all_points_x']
            py = obj['all_points_y']
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]

            x_min, y_min, x_max, y_max = (
                min(px), min(py), max(px), max(py))


            data_anno = dict(
                image_id=idx,
                id=obj_count,
                category_id=0,
                bbox=[x_min, y_min, x_max - x_min, y_max - y_min],
                area=(x_max - x_min) * (y_max - y_min),
                segmentation=[poly],
                iscrowd=0)
            annotations.append(data_anno)
            obj_count += 1

    coco_format_json = dict(
        images=images,
        annotations=annotations,
        categories=[{'id':0, 'name': 'balloon'}])
    mmcv.dump(coco_format_json, out_file)

if __name__ == '__main__':
    print(os.getcwd())
    # Confirm the junction to(e.g, [o:\datasets\balloon-v1]
    dsbase="fusen/ds"
    # annot-v1.1 means major.minor = [dataset version].[annotation version]
    annotversion = "1.1" 
    convert_balloon_to_coco(f"{dsbase}/train/via_region_data.json",f"fusen/annot-v{annotversion}/train.json",f"{dsbase}/train")
    convert_balloon_to_coco(f"{dsbase}/val/via_region_data.json", f"fusen/annot-v{annotversion}/val.json",f"{dsbase}/val")
