from pathlib import Path
import os
src = "./all_data"
des = "./coco"

des_images = os.path.join(des, "images")
os.makedirs(des_images, exist_ok=True)

des_labels = os.path.join(des, "labels")
os.makedirs(des_labels, exist_ok=True)

src = Path(src)
des = Path(des)

des_images = Path(des_images)
des_labels = Path(des_labels)

missing = []
for dataset in src.iterdir():
    dataset_name = dataset.name
    des_img_path = des_images / dataset_name
    des_label_path = des_labels / dataset_name
    des_img_path.mkdir()
    des_label_path.mkdir()

    src_img_path = dataset / "images"
    src_label_path = dataset / "labels"

    for f in src_img_path.iterdir():
        file_name, ext = f.name.rsplit(".")
        counterpart = src_label_path / (file_name + ".txt")
        if not counterpart.exists():
            missing.append(str(f))
        f.rename(des_img_path / f.name)
        counterpart.rename(des_label_path / counterpart.name)
