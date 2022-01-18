from glob import glob
import yaml
from sklearn.model_selection import train_test_split

img_list = glob('yolov5/yolo/yolo_data/*.jpg')
train_img_list, val_img_list = train_test_split(img_list, test_size=0.2, random_state=2000)

with open('yolov5/yolo/train.txt', 'w') as f:
  f.write('\n'.join(train_img_list) + '\n')

with open('yolov5/yolo/val.txt', 'w') as f:
  f.write('\n'.join(val_img_list) + '\n')

data = {'train': 'yolo/train.txt', 'val': 'yolo/val.txt', 'nc': 1, 'names': ['stop']}
with open('yolov5/yolo/data.yaml', 'w') as f:
  yaml.dump(data, f)
