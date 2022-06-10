from pathlib import Path
import os

root = "./all_data"
NEEDED_CLASSES = ["helmet", "no_helmet", "person"]
sum_dataset = Path("./sum_dataset")
sum_img = sum_dataset / "images"
sum_label = sum_dataset / "labels"

def classes_mapping(p):
    with open(str(p), "r") as f:
        names = [x.strip() for x in f]
    return names

def process_single(path: Path, merge=False):
    img_path = path / "images"
    labels_path = path / "labels"


    iter = labels_path.iterdir()
    class_txt = next(iter)
    assert class_txt.name.startswith("classes")
    classes = classes_mapping(str(class_txt))
    dropped = 0
    while True:
        file = next(iter, None)
        if not file:
            break
        try:
            new_content = []
            file_name = file.name
            file_path = str(file)
            with open(file_path) as f:
                for line in f:
                    l = line.strip().split()
                    lbl = classes[int(l[0])]
                    if lbl in NEEDED_CLASSES:
                        l[0] = str(NEEDED_CLASSES.index(lbl))
                        new_content.append(" ".join(l) + '\n')
            # file.unlink()
            img_counterpart = (img_path / file_name).with_suffix(".jpg")
            if new_content:
                with open(file_path, "w") as f:
                    for line in new_content:
                        f.write(line)
                if img_counterpart.exists():
                    file.rename(sum_label / file_name)
                    img_counterpart.rename((sum_img / file_name).with_suffix(".jpg"))
            else:
                file.unlink()
                if img_counterpart.exists():
                    img_counterpart.unlink()
                dropped += 1
        except Exception as e:
            print(e)


if __name__ == "__main__":
    for p in Path(root).iterdir():
        process_single(p)


