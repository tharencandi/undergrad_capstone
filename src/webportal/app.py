from flask import Flask, request, jsonify, send_file, g, render_template
from celery import Celery
from os import listdir, mkdir, remove, rename
from os.path import isfile, join, exists, expanduser
from datetime import datetime
import zipfile
import uuid
import json
import shutil
import sys, os
cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))

from image_tools.conversion import svs_to_png, svs_to_tiff


app = Flask(__name__, static_url_path='',
                  static_folder='frontend/build',
                  template_folder='frontend/build')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

home = expanduser("~")
WEB_PORTAL_DIR=join(home, ".glioblastoma_portal", "")
DATA_DIR = join(WEB_PORTAL_DIR, "scans/")
valid_extensions = ["png", "svs", "tif"]


# DATABASE = '/home/haeata/.glioblastoma_portal/file.db'

# def query_db(query, args=(), one=False):
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
  
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def init_db_if_not_exists():
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read()) 
#         db.commit()

# get specific file path,
def get_file(name, ext):
    dir_path = DATA_DIR + name
    file_path = "{}/{}.{}".format(dir_path,name ,ext)

    return file_path

# get meta file, returns path to meta file
def get_meta(id):
    meta_path = DATA_DIR+ id + '/' + id + ".meta"
    return meta_path

# save file object into file system
def save_file(file_obj, id, ext):

    dir_path = DATA_DIR + id
    file_path = "{}/{}.{}".format(dir_path,id,ext)
    file_obj.save(file_path)

# set web portal directory
@app.post('/dir')
def change_dir():
    dir = request.args['dir']

    if dir[-1] != '/':
        dir = dir + '/'

    WEB_PORTAL_DIR = dir
    return jsonify("DONE")

# get web portal directory
@app.get('/dir')
def get_dir():
    return jsonify(DATA_DIR)

# home page
@app.get('/')
def index():
    return render_template("index.html")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@app.get('/all')
def all_scans():
    scans = [f for f in listdir(DATA_DIR) if not isfile(join(DATA_DIR, f))]
    
    scan_list = []
    # return jsonify("a1")
    for id in scans:
        scan_id = id
        extensions = []
        date = ""
        dir_path = "{}{}/".format(DATA_DIR,id)

        # get extensions
        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

        for file in files:
            ext = file[-3:]
            if ext in valid_extensions:
                extensions.append(ext)

        # get date
        meta = get_meta(id)
        meta_data = open(meta, "r")
        data = json.load(meta_data)

        meta_data.close()
        scan_list.append(data)
    
    return jsonify(scan_list)

# download specified scan as extension as zipped file
@app.get('/scan')
def get_scan():
    #

    ids = request.args["ids"]
    ext = request.args["extension"]

    # check if directory exists, create if not
    dir_path = join(DATA_DIR, ids)
    file_path = "{}/{}.{}".format(dir_path,ids,ext)
    file_path = get_file(ids, ext)

    if not exists(file_path):
        return jsonify("File not Found: "+ file_path)
    
    # change status
    meta_path = dir_path + '/' + ids + '.meta'
    meta_path = get_meta(ids)
    # for id in ids:
    for i in range(0, len(ids)):

        # check if directory exists, create if not
        dir_path = DATA_DIR + ids[i]
        file_path = "{}/{}.{}".format(dir_path,ids[i],ext[i])

        if not exists(file_path):
            return jsonify("File not Found: "+ file_path)
        
        else:
            filenames.append(file_path)
            files.append((dir_path, i))

            # change status
            meta_path = dir_path + '/' + ids[i] + '.meta'

            with open(meta_path, 'r') as f:
                data = json.load(f)
            
            key = ext[i] + "Status"
            data[key] = "inProgress"

            with open(meta_path, 'w') as json_file:
                json.dump(data, json_file)

    with zipfile.ZipFile("multiple_files.zip", mode="w") as archive:
        for filename in filenames:
            archive.write(filename)
    
    # change status back
    for file in files:
        dir_path = file[0]
        i = file[1]
        meta_path = dir_path + '/' + ids[i] + '.meta'

        with open(meta_path, 'r') as f:
            data = json.load(f)
        
        key = ext + "Status"
        data[key] = "inProgress"

        with open(meta_path, 'w') as json_file:
            json.dump(data, json_file)

    with open(meta_path, 'r') as f:
            data = json.load(f)
        
    key = ext + "Status"
    data[key] = "Completed"

    with open(meta_path, 'w') as json_file:
        json.dump(data, json_file)
    
    return send_file(file_path)


# upload a new scan
@app.post('/scan')
def upload():

    file = request.files['file']
    filename = file.filename

    if filename == '':
        return jsonify("NULL")

    print(filename)
    id = filename.split(".")[0]
    print(id)
    print(filename)
    ext = filename.split(".")[-1]
    print(ext)
    file_id = str(uuid.uuid4())
    if ext not in valid_extensions:
        return jsonify("INVALID FILE FORMAT: {}".format(ext))

    # check if directory exists
    dir_path = DATA_DIR + file_id
    path = dir_path

    counter = 1
    while exists(dir_path):
        dir_path = path + "(" + str(counter) + ")"
        counter += 1

    id = dir_path.split('/')[-1]
    file_path = "{}/{}.{}".format(dir_path,file_id,ext)
    
    mkdir(dir_path)

    
    now = datetime.now()
    
    meta_data = {
        'fileId': str(file_id),
        "fileName": filename,
        "created": now.strftime("%d/%m/%Y %H:%M:%S"),
        "tifStatus": "none",
        "pngStatus": "none",
        "maskStatus": "none",
        "downloadStatus": "none"
    }

    with open("{}/{}.meta".format(dir_path,file_id), 'w') as json_file:
        json.dump(meta_data, json_file)

    save_file(file, id, ext)
    return jsonify(str(file_uuid))

# delete scan
@app.delete('/scan')
def delete():

    # ids = request.args.getlist("ids")
    id = request.args["ids"]

    dir_path = DATA_DIR + id
    # file_path = "{}/{}.{}".format(dir_path,ids,ext)

    try:
        shutil.rmtree(dir_path)
        return jsonify("DONE")
    except Exception as e:
        return jsonify(e)

@app.put('/scan')
def scan_rename():
    id = request.args["ids"]
    new_name = request.args["new_name"]

    for id in ids:
        dir_path = DATA_DIR + id

    # meta_file = dir_path + id + ".meta"
    meta_path = dir_path + '/' + id + '.meta'

    with open(meta_path, 'r') as f:
            data = json.load(f)
        
    new_dir = DATA_DIR + new_name
    rename(dir_path, new_dir)
    
    return jsonify("DONE")
    
PNG_EXT=".png"
TIF_EXT=".tif"
MASK_EXT=".mask"
META_EXT=".meta"
SVS_EXT=".svs"

def make_fpath(uuid, ext):
    return os.path.join(DATA_DIR, uuid, uuid + ext)

def get_svs_dir(uuid):
    return os.path.join(DATA_DIR, uuid, "")

def set_meta_field(uuid, field, value):
    fpath = make_fpath(uuid, META_EXT)
    meta = None
    with open(fpath) as f:
        meta = json.loads(f)
        meta[field] = value
    
    if meta:
        with open(fpath) as o:
            json.dump(meta, o)

@celery.task()
def make_png(self, uuid, svs_fpath, dest):
    set_meta_field(uuid, "pngStatus", "inProgress")
    res = svs_to_png(svs_fpath, dest)
    if res != image_tools.GOOD:
        set_meta_field(uuid, "pngStatus", "failed")
    set_meta_field(uuid, "pngStatus", "completed")
    return
@celery.task()
def make_tif(self, uuid, svs_fpath, dest):
    set_meta_field(uuid, "tifStatus", "inProgress")
    res = svs_to_tiff(svs_fpath, dest)
    if res != image_tools.GOOD:
        set_meta_field(uuid, "tifStatus", "failed")
    set_meta_field(uuid, "tifStatus", "completed")
    return
 
@celery.task()
def make_mask(self, uuid, svs_fpath, dest):
    time.sleep(60)
    return

TASK_MAP = {
    PNG_EXT: make_png,
    TIF_EXT: make_tif,
    MASK_EXT: make_mask
}


# run algo, generate mask
@app.post('/generate')
def generate():
    target_svs = request.json["ids"]
    target_exts = request.json["exts"]
    
    res = {
        "ids": []
    }
    for target in target_svs:
        if exists(get_svs_dir(target)):
            res["ids"].append(target)
            for e in target_exts:
                TASK_MAP[e].delay(target, make_fpath(target, SVS_EXT), make_fpath(target, e))
    return jsonify(res), 200



if __name__ == '__main__':
    print(sys.path)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)

