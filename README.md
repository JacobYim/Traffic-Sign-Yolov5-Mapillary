# Traffic-Sign-Yolov5-Mapillary

## Dataset
```
wget https://drive.google.com/file/d/19G3ks3sA6Dxz4cJBiDJHt2iuhR8Gur4z/view?usp=sharing
mkdir dataset
unzip organized_mapilary_dataset.zip -d dataset
rm organized_mapilary_dataset.zip
python dataset_converter.py  # generating yolo/yolo_data
```

## Training
```
pip install -r requirements.txt
python config_generator.py
git clone https://github.com/ultralytics/yolov5.git
cd yolov5/
pip install -r requirements.txt
```

### start training
```
python train.py --img 416 --batch 16 --epochs 50 --data ../yolo/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name gun_yolov5s_results
```

## Test
```
%load_ext tensorboard
%tensorboard --logdir /content/yolov5/runs/
```

```
from IPython.display import Image
import os

val_img_path = val_img_list[1]

!python detect.py --weights /content/yolov5/runs/train/gun_yolov5s_results/weights/best.pt --img 416 --conf 0.5 --source "{val_img_path}"

Image(os.path.join('/content/yolov5/inference/output', os.path.basename(val_img_path)))
```