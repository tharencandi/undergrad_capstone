import os
import json
from  datetime import datetime

META_DATA_FORMAT = {
        'fileId': '',
        'caseType': '',
        "fileName": '',
        "dirPath": '',
        "filePath": '',
        "created": '',
        "tifStatus": "none",
        "tifJobId": "",
        "pngStatus": "none",
        "pngJobId": "",
        "maskStatus": "none",
        "maskJobId": "" 
    }
def get_meta_path(uuid, meta_dir):
    return os.path.join(meta_dir, uuid+".meta")
   
def set_meta_field(uuid, field, value, meta_dir):
    fpath =get_meta_path(uuid, meta_dir)
    # print(fpath)
    meta = None
    with open(fpath, "r") as f:
        meta = json.loads(f.read())
        meta[field] = value
    
    if meta:
        with open(fpath, "w") as o:
            json.dump(meta, o)

def get_meta_field(uuid, field, meta_dir):
    fpath = get_meta_path(uuid, meta_dir)
    meta = None
    with open(fpath, "r") as f:
        meta = json.loads(f.read())
    
    if meta:
        return meta[field]

def make_meta(uuid, meta_dir, **kwargs):
    if not os.path.exists(get_meta_path(uuid, meta_dir)):
        with open(get_meta_path(uuid, meta_dir), "w") as f:
            json.dump(META_DATA_FORMAT, f)
    for k, v in kwargs.items():
        set_meta_field(uuid, k, v, meta_dir)
    
    if 'created' not in kwargs:
        set_meta_field(uuid, 'created', datetime.fromtimestamp(os.path.getctime(get_meta_path(uuid, meta_dir))).strftime('%Y-%m-%d %H:%M:%S'), meta_dir)