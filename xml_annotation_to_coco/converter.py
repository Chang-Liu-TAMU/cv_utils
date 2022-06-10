from pathlib import Path
import os
from tqdm import tqdm
import xml.etree.ElementTree as ET
import multiprocessing as mlp

names = ["helmet", "no_helmet", "background"]  # class names
yaml = {"path": [], "names": names}


des_root = "./target_dir"

for i in ["images", "labels"]:
    p = os.path.join(des_root, i)
    if not os.path.exists(p):
        os.mkdir(p)

def convert_label(path, lb_path, image_id):
  def convert_box(size, box):
      dw, dh = 1. / size[0], 1. / size[1]
      x, y, w, h = (box[0] + box[1]) / 2.0 - 1, (box[2] + box[3]) / 2.0 - 1, box[1] - box[0], box[3] - box[2]
      return x * dw, y * dh, w * dw, h * dh

  in_file = open(path / f'Annotations/{image_id}.xml')
  out_file = open(lb_path, 'w')
  tree = ET.parse(in_file)
  root = tree.getroot()
  size = root.find('size')
  w = int(size.find('width').text)
  h = int(size.find('height').text)

  for obj in root.iter('object'):
      cls = obj.find('name').text
      if cls in yaml['names'] and not int(obj.find('difficult').text) == 1:
          xmlbox = obj.find('bndbox')
          bb = convert_box((w, h), [float(xmlbox.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')])
          cls_id = yaml['names'].index(cls)  # class id
          out_file.write(" ".join([str(a) for a in (cls_id, *bb)]) + '\n')

def converter(root: Path, des_path: str):
    """
    :param path: such as Path("./dataset/VOC2022")
    :param des_path: such as "./"target_dir"
    :return:
    """
    dataset_name = root.name
    des_path = Path(des_path)
    for image_set in ["train", "val", "test"]:
        try:
            image_ids = open(str(root / f"ImageSets/Main/{image_set}.txt")).read().strip().split()
        except Exception as e:
            print(e)
            print(f"{dataset_name}-{image_set}-does not exists, ignore it")
            continue

        des_img_path = des_path / "images" / f"{dataset_name}_{image_set}"
        des_label_path = des_path / 'labels' / f"{dataset_name}_{image_set}"
        if not des_img_path.exists():
            des_label_path.mkdir()
        else:
            return
        if not des_label_path.exists():
            des_label_path.mkdir()
        # path.mkdir(exist_ok=True, parents=True)
        missing = 0
        for id in tqdm(image_ids, desc=f'{dataset_name}-{image_set}'):
            try:
                f = root / f'JPEGImages/{id}.jpg'  # old img path
                lb_path = (des_label_path / f.name).with_suffix('.txt')  # new label path
                if f.exists() and lb_path.exists():
                    f.rename(des_label_path / f.name)  # move image
                    convert_label(root, lb_path, id)  # convert labels to YOLO format
            except:
                missing += 1
        if missing:
            print(f"missing num of {dataset_name} -- {image_set} : {missing}")

if __name__ ==  "__main__":
    src_root = Path("./dataset")
    pool = []
    for dataset in src_root.iterdir():
        pool.append(mlp.Process(target=converter, args=(dataset, des_root)))
    l = [p.start() for p in pool]
    print("all done")
