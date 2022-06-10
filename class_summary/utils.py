# @Time: 2022/6/2 9:53
# @Author: chang liu
# @Email: chang_liu_tamu@gmail.com
# @File:utils.py
from pathlib import Path
import json
import logging
from collections import defaultdict
from typing import List, Dict

logger = logging.getLogger("My logger")

srcs = ["D:\ShangHai\Annotation\labelled\zonghe_0609\zonghe_0609"]

summary_dict = defaultdict(int)

def english_chinese_mapping(path="./classes.txt"):
    class_dict = {}
    with open(path, "r", encoding="utf-8") as f:
        for en, cn in [x.strip().split() for x in f]:
            class_dict[en] = cn
    return class_dict

def translate(d):
    cn_class_dict = english_chinese_mapping()
    return {cn_class_dict[key]: val for key, val in d.items() if key in cn_class_dict}

def read_classes(path):
    with open(path, "r") as f:
        l = [i.strip() for i in f]
    d = {key: l[key] for key in range(len(l))}
    print(f"total classes num: {len(l)}")
    return d

def accumulate_classes(path: Path, label_mapping: Dict):
    global summary_dict
    with open(str(path), "r") as f:
        for line in f:
            cls = int(line.strip().split()[0])
            summary_dict[label_mapping[cls]] += 1



def read_sinle_annotation(path):
    p = Path(path)
    labels = p / "labels"
    iter = labels.iterdir()
    classes_txt = next(iter)
    assert classes_txt.name.startswith("class")
    label_mapping = read_classes(str(classes_txt))
    for label in iter:
        accumulate_classes(label, label_mapping)

# read_sinle_annotation(srcs[0])

def read_all_annotations(paths):
    for p in paths:
        read_sinle_annotation(p)

read_all_annotations(srcs)
# print(f"classes_num: {len(summary_dict)}", summary_dict)
# print(translate(summary_dict))
d = {}
d["总数"] =sum(summary_dict.values())
# d["图片总数"] = 500
d["标签"] = translate(summary_dict)
j = json.dumps(d, ensure_ascii=False, indent=4)
# print(type(j))
# print(j)
with open("label_summary_06_09_extra.json", "w", encoding="utf-8") as f:
    f.write(j)







