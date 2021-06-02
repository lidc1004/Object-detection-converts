import os
import os.path
from tqdm import tqdm
from xml.etree.ElementTree import parse, Element

def changeName(xml_fold, origin_name, new_name):
    
    files = os.listdir(xml_fold)
    cnt = 0 
    for xmlFile in tqdm(files):
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):
            tmp_name = obj.find('name').text
            if tmp_name == origin_name: 
                obj.find('name').text = new_name
                #print("change %s to %s." % (origin_name, new_name))
                cnt += 1
        dom.write(file_path, xml_declaration=True)
    print("%d changed" % cnt)

def changeAll(xml_fold,new_name):
    
    files = os.listdir(xml_fold)
    cnt = 0 
    for xmlFile in tqdm(files):
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):
            tmp_name = obj.find('name').text
            obj.find('name').text = new_name
            print("change %s to %s" % (tmp_name, new_name))
            cnt += 1
        dom.write(file_path, xml_declaration=True)
    print("%d changed" % cnt)

def countAll(xml_fold):
    
    files = os.listdir(xml_fold)
    dict={}
    for xmlFile in tqdm(files):
        file_path = os.path.join(xml_fold, xmlFile)
        dom = parse(file_path)
        root = dom.getroot()
        for obj in root.iter('object'):
            tmp_name = obj.find('name').text
            if tmp_name not in dict:
                dict[tmp_name] = 0
            else:
                dict[tmp_name] += 1
        dom.write(file_path, xml_declaration=True)
    print("numbers :")
    print("-"*10)
    for key,value in dict.items():
        print("class : %s numbers : %d " % (key, value))
    print("-"*10)


if __name__ == '__main__':
    path = "output/coco/val/Annotations/"
    changeName(path, "n04381587", "n0123")
    countAll(path)

