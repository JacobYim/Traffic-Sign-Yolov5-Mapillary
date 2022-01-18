import os 
import shutil
import cv2
import json
import pandas as pd
from PIL import Image
from functools import *

destination_dataset_dir_name  = "yolov5/yolo/yolo_data"
source_dataset_dir_name = "yolov5/dataset"

def load_mapilary(dataset='total') :
    json_datas = []
    if dataset == 'total' or dataset == 'fully' : 
        for label_json in os.listdir(source_dataset_dir_name+'/organized_mapilary_dataset/fully/annotations') :
            with open(source_dataset_dir_name+'/organized_mapilary_dataset/fully/annotations/'+label_json) as json_stream:
                json_data = json_stream.read()
                json_data = json.loads(json_data)
                json_data['dataset'] = 'fully'
                json_data['filename'] = label_json.split('.')[0]
                json_datas.append(json_data)

    if dataset == 'total' or dataset == 'partially' :
        for label_json in os.listdir(source_dataset_dir_name+'/organized_mapilary_dataset/partially/annotations') :
            with open(source_dataset_dir_name+'/organized_mapilary_dataset/partially/annotations/'+label_json) as json_stream:
                json_data = json_stream.read()
                json_data = json.loads(json_data)
                json_data['dataset'] = 'partially'
                json_data['filename'] = label_json.split('.')[0]
                json_datas.append(json_data)
    return json_datas


def mapilary_to_yolo(mapilary_jsons, yolo_labels, mapilary_labels_list) :
    mapilary_labels = list(reduce(lambda x, y : x+y, mapilary_labels_list))
    target_data_jsons = list(filter(lambda map_jason : len(set(mapilary_labels) & set(map(lambda x : x['label'] , map_jason['objects']))) > 0, mapilary_jsons))
    label_matching = open("label_matching.txt", "a")
    for data in target_data_jsons :
        try :
            shutil.copy(source_dataset_dir_name+'/organized_mapilary_dataset/'+data['dataset']+'/img/'+data['filename']+'.jpg', destination_dataset_dir_name)
            f = open(destination_dataset_dir_name+'/'+data['filename']+'.txt', "a")
           # for i, (yolo_label, mapilary_labels) in enumerate(zip(yolo_labels, mapilary_labels_list)) :
            for i, yolo_label, mapilary_labels in zip(list(range(len(yolo_labels))), yolo_labels, mapilary_labels_list) :
                label_matching.write("{} : {}".format(i, yolo_label))
                for data_object in data['objects'] :
                    if data_object['label'] in mapilary_labels :
                        # save annotation at destination directory
                        content_txt = " ".join([str(i), str(data_object['bbox']['xmin']), str(data_object['bbox']['ymin']), str(data_object['bbox']['xmax']), str(data_object['bbox']['ymax'])])
                        f.write(content_txt+'\n')
            f.close()
        except :
            pass
    #label_matching.close()

def convert_coordinate() :
    print('convert_coordinate start')
    new_label_file_dir = "yolov5/yolo/yolo_data"
#    if new_label_file_dir in os.listdir() :
#        shutil.rmtree(new_label_file_dir)
#    os.mkdir(new_label_file_dir)

    filelist = os.listdir(destination_dataset_dir_name)
    textfilelist = list(filter(lambda x : '.txt' in x, filelist))
    for textfile in textfilelist :
        print('{} processing ...'.format(destination_dataset_dir_name+"/"+textfile))
        file = open(destination_dataset_dir_name+"/"+textfile,mode='r+')
        all_of_it = file.read()
        lines = all_of_it.split('\n')[:-1]  
        file.close()
        
        print(lines)

        im = cv2.imread(destination_dataset_dir_name+'/'+textfile.split('.txt')[0]+'.jpg')
        h, w, c = im.shape
        # print(h, w, c)

        new_file = open(new_label_file_dir+"/"+textfile, "w+")
        for line in lines :
            # print(line)
            content = line.split(' ')
            min_x = float(content[1]) 
            min_y = float(content[2])
            max_x = float(content[3])
            max_y = float(content[4])
            content[1] = str(min_x/w)
            content[2] = str(min_y/h)
            content[3] = str((max_x-min_x)/w)
            content[4] = str((max_y-min_y)/h)
            print("print content : ", content)
            new_line = " ".join(content)+"\n"
            # print(new_line)
            new_file.write(new_line)
        new_file.close()






if __name__ == "__main__" :    
    with open('label_setting.json') as f:
        data = json.load(f)
    yolo_labels =  list(data.keys())
    mapilary_labels_list = list(map(lambda x : data[x]["mapilary_labels_list"], yolo_labels))

    if destination_dataset_dir_name in os.listdir() :
        shutil.rmtree(destination_dataset_dir_name)
    os.mkdir(destination_dataset_dir_name)
    mapilary_jsons = load_mapilary(dataset='fully')
    mapilary_to_yolo(mapilary_jsons, yolo_labels, mapilary_labels_list)
    convert_coordinate()