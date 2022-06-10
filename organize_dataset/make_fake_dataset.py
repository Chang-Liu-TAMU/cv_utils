from pathlib import Path
import os

root = "./all_data"
os.makedirs(root, exist_ok=True)
root = Path(root)
for d in ["data01", "data02", "data03"]:
    p = root / d
    p.mkdir()
    img = p / "images"
    labels = p / "labels"
    img.mkdir()
    labels.mkdir()
    for i in range(4):
        name = d + "_" + str(i)
        image = str(img / (name + ".jpg"))
        label = str(labels / (name + ".txt"))
        with open(image, "w"):
            pass
        with open(label, "w"):
            pass
