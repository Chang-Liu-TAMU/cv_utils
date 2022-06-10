from pathlib import Path
import os
import json
import cv2

label_path = "D:\ShangHai\crowehuman\\annotation_train.odgt"
assert os.path.exists(label_path), "invalid path"

count = 0
with open(label_path, "r") as f:
    while True:
        first = next(f, None)
        count += 1
        if not first:
            break
        first = first.strip()
        data = json.loads(first)
        # print(type(data))
        # json_data = json.dumps(data, indent=2)
        # print(type(json_data))
        id = data["ID"]
        # print(data)
        image_path = os.path.join("D:\ShangHai\crowehuman\CrowdHuman_train01\Images", id+".jpg")
        if os.path.exists(image_path):
            print(json.dumps(data, indent=2))
            img = cv2.imread(image_path)
            #with head shown
            print(img.shape)
            for obj in data["gtboxes"]:
                if obj["tag"] == "person":
                    x1, y1, dx, dy = obj["hbox"]
                    print(dx, dy)
                    cv2.rectangle(img, (x1, y1), (x1+dx, y1+dy), color=0xff)
            cv2.imshow("img", img)
            key = cv2.waitKey(0)
            if key & 0xff == ord("q"):
                cv2.destroyAllWindows()
            break
print(count)