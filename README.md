# Object detection converts

### Objects365 annotations 2 xml

##### 1. 数据准备

~Objects365`数据集共两个版本：2019 `Objects365`目标检测数据集，2020 `Objects365`物体检测数据集

- 2019版本官方不在提供下载，这里提供百度云盘下载地址：链接: [https://pan.baidu.com/s/1q1kpu1TWSobRhoXr-TE9PA](https://pan.baidu.com/s/1q1kpu1TWSobRhoXr-TE9PA) 提取码: qiva 
- 2020版本官方下载地址：[https://open.baai.ac.cn/data-set-enter-detail/12647](https://open.baai.ac.cn/data-set-enter-detail/12647)

注：数据转换使用2019版本

数据目录结构：

```
/path/to/objects365
    Annotations
        train
            train.json
        val
            val.json
    Images
        train
            *.jpg
        val
            *.jpg
```

数据标签对应参考：object365_dict.txt

##### 2. 数据处理

所需文件：obj365_main.py，object365_to_voc.py和object365_dict.txt

```python
python obj365_main.py -i "/obj365" -o "output/obj365" -c 80 92 97 
```

其中 -i 为数据集输入路径，-o为转换输出路径，-c为类别序号，对应在object365_dict.txt中，可根据实际情况进行选择。

##### 3. 数据输出

输出目录结构如下：

```
/path/to/output
    annotations_xml_train                   // 标注目录
        xxx.xml                             // 标注文件
        yyy.xml                             // 标注文件
    annotations_xml_val                     // 标注目录
        xxx.xml                             // 标注文件
        yyy.xml                             // 标注文件            
    annotations_xml_object365_train.txt          
    annotations_xml_object365_val.txt            
```

其中列表文件格式

```
   XML文件路径 图片路径 [类别1 类别2 ...]
```

XML文件路径为相对于输出目录的相对路径，图片路径为相对于输入目录的相对路径

### COCO annotations 2 xml

##### 1. 数据准备

- 官方下载地址：[https://cocodataset.org/#download](https://cocodataset.org/#download)
- COCO2017数据集目录结构如下：

```
/path/to/coco
    Annotations
        instances_train2017.json
        instances_val2017.json
    Images
        train2017
            *.jpg
        val2017
            *.jpg
```

##### 2. 数据处理

所需文件：coco_to_voc.py，coco_classes.txt

```
python coco_to_voc.py
```

其中数据集路径，数据保存路径以及训练集验证集可自行选择

##### 3. 数据输出

输出目录结构如下：

```
/path/to/output
   Annotations                             // 标注目录
        xxx.xml                             // 标注文件
        yyy.xml                             // 标注文件
   Iamges
        xxx.jpg
        yyy.jpg
```

### xml数据划分-xml_split.py

可自行划分训练集与验证集，也可使用官方划分方式，之后生成包含图片名称的train.txt,val.txt,test.txt,trainval.txt

### xml数据统计与改变标签名-xml_counter_change.py

可统计指定文件夹下所有xml数据，统计每个类别数量，也可改变一个或多个类别标签名，也可一次性全部更改

### xml数据转换为yolo格式的txt数据-voc_to_yolo.py

将xml数据转换为yolo所需的txt格式，其中需要将xml数据与图片数据放到各自的路径下，以及划分后的训练集，验证集文档

注：此部分采用官方VOC数据集的路径，需将数据放到指定文件下，也根据实际情况更改路径



