import json
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cv2
import shutil
import os
import subprocess
import argparse
import glob
from tqdm import tqdm
import time


# cellphone:79 key:266 handbag:13 laptop:77
# classes_names = {79: "cellphone", 266: "key", 13: "handbag", 77: "laptop"}
# classes_names = {79: "cell phone", 13: "handbag", 77: "laptop"}

def save_annotations(classes_names, anno_file_path, imgs_file_path, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset):
    print(classes_names)
    # open json file(val.json or train.json)
    print("json load:", anno_file_path)
    with open(anno_file_path, 'r') as f:
        data = json.load(f)
        # 900w+
        print("anno count:", len(data["annotations"]))
        print("image count:", len(data["images"]))

        
        img_map = {}
        img_2_anno = {}
        for i in data["images"]:
            img_map[i["id"]] = i
            img_2_anno[i["id"]] = []

        for anno in data["annotations"]:
            if anno["category_id"] in classes_names.keys():
                img_2_anno[anno["image_id"]].append(anno)

        for _, id in enumerate(img_2_anno):
            annos = img_2_anno[id]
            if len(annos) > 0:
                # print("id:", id, "annos:", annos)
                time_start = time.time()
                img = img_map[id]
                img_name = img["file_name"]
                img_width = img["width"]
                img_height = img["height"]

                objs = []
                for anno in annos:
                    # print("anno:", anno)
                    print(img["file_name"])
                    # img_path use to find the image path
                    # bbox
                    bbox = anno["bbox"]
                    xmin = max(int(bbox[0]), 0)
                    ymin = max(int(bbox[1]), 0)
                    xmax = min(int(bbox[2] + bbox[0]), img_width)
                    ymax = min(int(bbox[3] + bbox[1]), img_height)
                    class_name = classes_names[anno["category_id"]]
                    obj = [class_name, xmin, ymin, xmax, ymax]
                    objs.append(obj)
                
                save_head(objs, imgs_file_path, img_name, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset, img_width, img_height)

                time_end = time.time()
                print("img id", id, "time(s)", time_end - time_start)

    print(" conver is done ")


def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)

def write_txt(output_dir, anno_path, img_path, dataset):
    list_name = output_dir + '/annotations_xml_object_{}.txt'.format(dataset)
    if not os.path.exists(list_name):
        with open(list_name, 'w', encoding="utf=8") as fs:
            print(fs)
    with open(list_name, 'r', encoding='utf-8') as list_fs:
        with open(list_name, 'a+', encoding='utf-8') as list_f:
            lines = os.path.basename(anno_path) + "\t" + img_path + "\n"
            list_f.write(lines)


def write_xml(anno_path, objs, img_path, output_dir, head, objectstr, tailstr, dataset):
    print(anno_path)
    with open(anno_path, 'w') as f:
        f.write(head)
        for obj in objs:
            f.write(objectstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
        f.write(tailstr)
        write_txt(output_dir, anno_path, img_path, dataset)


def save_head(objs, imgs_file_path, img_name, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset, img_width, img_height):
    # imgs = cv2.imread(os.path.join(imgs_file_path, img_name))
    anno_path = os.path.join(output_anno_dir, img_name[:-3] + "xml")
    print("anno_path:", anno_path)

    # if (imgs.shape[2] == 1):
    #     print(img_name + " not a RGB image")
    #     return

    head = headstr % (img_name, img_width, img_height, 3)
    write_xml(anno_path, objs, img_name, output_dir, head, objectstr, tailstr, dataset)


def find_anno_img(input_dir):
    # According input dir path find Annotations dir and Images dir
    anno_dir = os.path.join(input_dir, "Annotations")
    img_dir = os.path.join(input_dir, "Images")
    return anno_dir, img_dir


def main_object365(classes, input_dir, output_dir, headstr, tailstr, objectstr):
    # use ids match classes
    classes_names = {}
    with open("./object365_dict.txt", 'r') as f:
        print(classes)
        for line in f:
            (key, value) = line.strip().split(":")
            if not classes:
                classes_names[int(key)] = value

            if key in classes:
                classes_names[int(key)] = value

    anno_dir, img_dir = find_anno_img(input_dir)
    for dataset in ["val", "train"]:
        # xml output dir path
        output_anno_dir = os.path.join(output_dir, dataset)
        if not os.path.exists(output_anno_dir):
            mkr(output_anno_dir)

        # read jsons file
        anno_file_path = os.path.join(anno_dir, dataset, dataset+".json")
        # read imgs file
        imgs_file_path = os.path.join(img_dir, dataset)
        save_annotations(classes_names, anno_file_path, imgs_file_path, output_anno_dir, output_dir,headstr, tailstr, objectstr, dataset)
