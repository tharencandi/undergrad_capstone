META_DATA_FORMAT = {
        'fileId': '',
        'case': '',
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
    return os.join(meta_dir, uuid)
   
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
    if not os.exists(get_meta_path(uuid, meta_dir)):
        with open(uuid+".meta", "w") as f:
            json.dump(META_DATA_FORMAT, f)
    for k, v in kwargs:
        set_meta_field(uuid, k, v, meta_dir)
    
    if 'created' not in kwargs:
        set_meta_field(uuid, 'created', datetime.fromtimestamp(file_create_date).strftime('%Y-%m-%d %H:%M:%S'), meta_dir)