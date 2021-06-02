#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import shutil

ann_filepath = "./co_val/annotations/"
img_filepath = './co_val/images/'
img_savepath = './obj365/JPEGImages_val/'
ann_savepath = './obj365/Annotations_val/'
if not os.path.exists(img_savepath):
     os.mkdir(img_savepath)
if not os.path.exists(ann_savepath):
    os.mkdir(ann_savepath)


#classes = ['apple', 'banana', 'tomato', 'pizza', 'lemon','potato','sausage','pie',
          # 'bread', 'donut', 'pumpkin', 'cookies', 'ice cream', 'carrot','hot dog',
           #'grapes', 'pear', 'orange', 'strawberry', 'cake','hamburger','egg',
           #'wild bird', 'cat', 'fish', 'cow', 'horse', 'sheep', 'elephant', 'zebra', 'giraffe',
           #'dog','mouse','duck','pigeon','goose','deer','chicken','penguin','bear','peach']

classes = ['person']

def save_annotation(file):

    tree = ET.parse(ann_filepath + '/' + file)
    root = tree.getroot()
    result = root.findall("object")
    bool_num = 0
    for obj in result:
         if obj.find("name").text not in classes:
             root.remove(obj)
         else:
            bool_num = 1
    if bool_num:
        tree.write(ann_savepath + file)
        return True
    else:
        return False


def save_images(file):
    name_img = img_filepath + os.path.splitext(file)[0] + ".jpg"
    shutil.copy(name_img, img_savepath)
    return True

count = 0
if __name__ == '__main__':
    for f in os.listdir(ann_filepath):
        if save_annotation(f):
            save_images(f)
            count +=1
print("counts:" + str(count))