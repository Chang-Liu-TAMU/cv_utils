import mxnet as mx
import mxnet.ndarray as nd
from skimage import io
import numpy as np
from mxnet import recordio
from tqdm import tqdm
import os

# path_prefix = "./fake_faces_glintasia/train"
path_prefix = "D:\ShangHai\Annotation\\faces_glintasia\\faces_glintasia"
output_dir = os.path.join(path_prefix, "data")

rec_path = os.path.join(path_prefix, "train.rec")
idx_path = os.path.join(path_prefix, "train.idx")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

imgrec = recordio.MXIndexedRecordIO(idx_path, rec_path, "r")
for i in tqdm(range(200)):
    header, s = recordio.unpack(imgrec.read_idx(i+1))
    img = mx.image.imdecode(s).asnumpy()
    label = str(header.label[0])
    label_dir = os.path.join(output_dir, label)
    if not os.path.exists(label_dir):
        os.mkdir(label_dir)

    fname = f"{label}_{i}.jpg"
    fpath = os.path.join(label_dir, fname)
    io.imsave(fpath, img)