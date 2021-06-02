# -*- coding:utf-8 -*-
# coco-process.py
from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import skimage.io as io
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw
 

dataDir = './COCO2017'
savepath = './output/coco/val/'
img_dir = savepath+'Images/'
anno_dir = savepath+'Annotations/'

datasets_list = ['val2017']
#datasets_list=['train2017']
 
classes_names = ['person','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe',
                 'frisbee','skis','snowboard','kite','baseball bat','baseball glove','skateboard',
                 'surfboard','tennis racket','banana','apple','sandwich','orange','broccoli','carrot',
                 'hot dog','pizza','donut','cake']

headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""
 
tailstr = '''\
</annotation>
'''
 
#if the dir is not exists,make it,else delete it
def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
mkr(img_dir)
mkr(anno_dir)
def id2name(coco):
    classes=dict()
    for cls in coco.dataset['categories']:
        classes[cls['id']] = cls['name']
    return classes
 
def write_xml(anno_path,head, objs, tail):
    f = open(anno_path, "w")
    f.write(head)
    for obj in objs:
        f.write(objstr%(obj[0], obj[1], obj[2], obj[3], obj[4]))
    f.write(tail)
 
 
def save_annotations_and_imgs(coco,dataset,filename,objs):
    #eg:COCO_train2014_000000196610.jpg-->COCO_train2014_000000196610.xml
    anno_path=anno_dir+filename[:-3]+'xml'
    img_path=dataDir+'/'+'Images'+'/'+dataset+'/'+filename
    print(img_path)
    print('step3-image-path-OK')
    dst_imgpath=img_dir+filename
 
    img=cv2.imread(img_path)
    if (img.shape[2] == 1):
        print(filename + " not a RGB image")
        return
    shutil.copy(img_path, dst_imgpath)
 
    head=headstr % (filename, img.shape[1], img.shape[0], img.shape[2])
    tail = tailstr
    write_xml(anno_path,head, objs, tail)
 
 
def showimg(coco,dataset,img,classes,cls_id,show=True):
    global dataDir
    I = Image.open('%s/%s/%s/%s'%(dataDir,'images',dataset,img['file_name']))
    print('step2-imageOpen-OK')
    annIds = coco.getAnnIds(imgIds=img['id'], catIds=cls_id, iscrowd=None)
    # print(annIds)
    anns = coco.loadAnns(annIds)
    # print(anns)
    # coco.showAnns(anns)
    objs = []
    for ann in anns:
        class_name = classes[ann['category_id']]
        if class_name in classes_names:
            print(class_name)
            if 'bbox' in ann:
                bbox = ann['bbox']
                xmin = int(bbox[0])
                ymin = int(bbox[1])
                xmax = int(bbox[2] + bbox[0])
                ymax = int(bbox[3] + bbox[1])
                obj = [class_name, xmin, ymin, xmax, ymax]
                objs.append(obj)
                #draw = ImageDraw.Draw(I)
                #draw.rectangle([xmin, ymin, xmax, ymax])
    # if show:
        # plt.figure()
        # plt.axis('off')
        # plt.imshow(I)
        # plt.show()
 
    return objs
 
for dataset in datasets_list:
    #set the annotations
    annFile = '{}/Annotations/instances_{}.json'.format(dataDir, dataset)
    print('step1-annFile-OK')
    #COCO API for initializing annotated data
    coco = COCO(annFile)
    
    #show all classes in coco
    classes = id2name(coco)
    print(classes)
    #[1, 2, 3, 4, 6, 8] ->classes_names
    classes_ids = coco.getCatIds(catNms=classes_names)
    print(classes_ids)
    for cls in classes_names:
        #Get ID number of this class
        cls_id = coco.getCatIds(catNms=[cls])
        img_ids = coco.getImgIds(catIds=cls_id)
        print(cls, len(img_ids))
        # imgIds=img_ids[0:10]
        for imgId in tqdm(img_ids):
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            print(filename)
            objs = showimg(coco, dataset, img, classes, classes_ids, show=False)
            print(objs)
            save_annotations_and_imgs(coco, dataset, filename, objs)