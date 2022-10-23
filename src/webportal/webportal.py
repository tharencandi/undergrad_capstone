from flask import Flask, request, jsonify, send_file, g, render_template
from celery import Celery
from os import listdir, mkdir, remove, rename
from os.path import isfile, join, exists, expanduser, getctime, dirname, realpath
from datetime import datetime
import zipfile
import uuid
# from Crypto.Hash import SHA256
import json
import shutil
import sys, os
cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))

# from image_tools.conversion import svs_to_png, svs_to_tiff
# from image_tools.conversion import GOOD


application = Flask(__name__, static_url_path='',
                  static_folder='frontend/build',
                  template_folder='frontend/build')

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

print(application.name)
celery = Celery("webportal", broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)

home = expanduser("~")
WEB_PORTAL_DIR =join(home, ".glioblastoma_portal", "")
DATA_DIR = join(WEB_PORTAL_DIR, "scans/")
# WEB_PORTAL_DIR = DATA_DIR

dir = dirname(realpath(__file__))
META_DIR = join(dir, '/meta_files')
META_DIR = dir + '/meta_files'
valid_extensions = ["png", "svs", "tif"]

# ~/test/

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

# @application.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

# def init_db_if_not_exists():
#     with application.app_context():
#         db = get_db()
#         with application.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read()) 
#         db.commit()

# def make_file_id(fname):
#     base = fname.split(".")[:-1]
#     base = "".join(base)
#     h = SHA256.new()
#     h.update(base.encode())
#     return h.hexdigest()

# get specific file path,
def get_file(uuid, ext):
    dir_path = DATA_DIR + uuid

    # files = [f for f in listdir(dir_path) if isfile(join(DATA_DIR, f))]

    # print(files)
    name = ''
    for f in listdir(dir_path):
        if f.endswith(ext):
            name = f
            break

    if name == '':
        print("errorrrr")
        return

    # file_path = "{}/{}.{}".format(dir_path,name ,ext)
    file_path = "{}/{}".format(dir_path,name)
    print(file_path)


    return file_path

def make_id(fname):
    base = fname.split(".")[:-1]
    base = "".join(base)
    return base

# get meta file, returns path to meta file
def get_meta(uuid):

    # dir_path = join(DATA_DIR, uuid) + '/'

    # files = [f for f in listdir(dir_path) if isfile(join(DATA_DIR, f))]
    # meta_file = ''
    
    # for f in listdir(dir_path):
    #     # print(f)
    #     if f.endswith("meta"):
    #         meta_file = f
    #         break;

    
    # if meta_file == '':
    #     print("no meta")
    #     return ''

    # meta_path = DATA_DIR+ uuid + '/' + meta_file


    meta_path = join(META_DIR, uuid + '.meta')
    if exists(meta_path):

        return meta_path
    else:
        return ""


# save file object into file system
def save_file(file_obj, id, ext, uuid):

    dir_path = DATA_DIR + uuid
    file_path = "{}/{}.{}".format(dir_path,id,ext)

    file_obj.save(file_path)
    return file_path

def create_meta(uuid, file_name, dir_path):

    file_path = join(dir_path, file_name) + '.svs'

    file_create_date = getctime(file_path)

    meta_data = {
        'fileId': uuid,
        # "fileName": filename,
        "fileName": file_name,
        # "created": now.strftime("%d/%m/%Y %H:%M:%S"),
        # "created": file_create_date,
        "created": datetime.fromtimestamp(file_create_date).strftime('%Y-%m-%d %H:%M:%S')
,
        "tifStatus": "none",
        "pngStatus": "none",
        "maskStatus": "none",
        "downloadStatus": "none"
    }

    with open("{}/{}.meta".format(META_DIR, uuid), 'w') as json_file:
        json.dump(meta_data, json_file)
    
    # 


# set web portal directory
@application.post('/dir')
def change_dir():
    global DATA_DIR

    print(DATA_DIR)
    dir = request.args['dir']

    if dir[-1] != '/':
        dir = dir + '/'

    DATA_DIR = dir

    return jsonify("DONE")

# get web portal directory
@application.get('/dir')
def get_dir():

    return jsonify(DATA_DIR)

# home page
@application.get('/')
def index():
    return render_template("index.html")

@application.get('/update')
def check_updates():

    for dir in listdir(DATA_DIR):
        dir_path = join(DATA_DIR, dir)

        exts = []

        if isfile(dir_path):
            continue
            
        svs_path =  ''
        meta_exists = False
        for scan_dir in listdir(dir_path):

            # files in uuid directory
            # check if svs file exists first
            if scan_dir.endswith("svs"):
                svs_path = scan_dir

                # remove .svs from end
                svs_path = svs_path[:len(svs_path)-4]
            
            elif scan_dir.endswith("tif"):
                exts.append("tif")
            elif scan_dir.endswith("mask"):
                exts.append("mask")
            elif scan_dir.endswith("png"):
                exts.append("png")  


            # check if meta file exists
            meta_path = get_meta(scan_dir)

            if meta_path != '':
                # meta exists
                # check for updates
                meta_exists = True
        
        if svs_path == '':
            # svs doesnt exist
            continue
        
        if meta_exists:
            # check for updates
            with open(meta_path, 'r') as f:
                data = json.load(f)
                
            # key = ext + "Status"
            # data[key] = "completed"
            for ext in exts:
                key = ext + "Status"
                if data[key] == 'none':
                    data[key] = 'completed'

            with open(meta_path, 'w') as json_file:
                json.dump(data, json_file)


        else:
            # create meta
            create_meta(dir, svs_path, dir_path)
            meta_path = get_meta(dir)
            with open(meta_path, 'r') as f:
                data = json.load(f)
            
            for ext in exts:
                key = ext + "Status"
                data[key] = "completed"

            with open(meta_path, 'w') as json_file:
                json.dump(data, json_file)
    return jsonify("DONE")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@application.get('/all')
def all_scans():
    # check for updates first
    for dir in listdir(DATA_DIR):
        dir_path = join(DATA_DIR, dir)

        exts = []

        if isfile(dir_path):
            continue
            
        svs_path =  ''
        meta_exists = False
        for scan_dir in listdir(dir_path):

            # files in uuid directory
            # check if svs file exists first
            if scan_dir.endswith("svs"):
                svs_path = scan_dir

                # remove .svs from end
                svs_path = svs_path[:len(svs_path)-4]
            
            elif scan_dir.endswith("tif") or scan_dir.endswith("tiff"):
                exts.append("tif")
            elif scan_dir.endswith("mask"):
                exts.append("mask")
            elif scan_dir.endswith("png"):
                exts.append("png")  


            # check if meta file exists
            meta_path = get_meta(scan_dir)

            if meta_path != '':
                # meta exists
                # check for updates
                meta_exists = True
        
        if svs_path == '':
            # svs doesnt exist
            continue
        
        if meta_exists:
            # check for updates
            with open(meta_path, 'r') as f:
                data = json.load(f)
                
            # key = ext + "Status"
            # data[key] = "completed"
            for ext in exts:
                key = ext + "Status"
                if data[key] == 'none':
                    data[key] = 'completed'

            with open(meta_path, 'w') as json_file:
                json.dump(data, json_file)


        else:
            # create meta
            create_meta(dir, svs_path, dir_path)
            meta_path = get_meta(dir)
            with open(meta_path, 'r') as f:
                data = json.load(f)
            
            for ext in exts:
                key = ext + "Status"
                data[key] = "completed"

            with open(meta_path, 'w') as json_file:
                json.dump(data, json_file)


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

        meta = get_meta(id)

        meta_data = open(meta, "r")
        data = json.load(meta_data)

        meta_data.close()
        scan_list.append(data)
    
    json_obj = {}
    
    for scan in scan_list:

        id = scan["fileId"]
        json_obj[id] = scan
    # return jsonify(scan_list)
    # print(jsonify(json_obj))

    return jsonify(json_obj)
    # return json_obj

# download specified scan as extension as zipped file
@application.get('/scan')
def get_scan():
    #
    ids = request.args["ids[]"]
    ext = request.args["extension[]"]

    # check if directory exists, create if not
    dir_path = join(DATA_DIR, ids)
    file_path = "{}/{}.{}".format(dir_path,ids,ext)
    file_path = get_file(ids, ext)

    if not exists(file_path):
        return jsonify("File not Found: "+ file_path)
    
    else:
        # change status
        meta_path = get_meta(ids)

        with open(meta_path, 'r') as f:
            data = json.load(f)
        
        key = ext + "Status"
        data[key] = "inProgress"

        with open(meta_path, 'w') as json_file:
            json.dump(data, json_file)


    with open(meta_path, 'r') as f:
            data = json.load(f)
        
    key = ext + "Status"
    data[key] = "completed"

    with open(meta_path, 'w') as json_file:
        json.dump(data, json_file)

    return send_file(file_path)


# upload a new scan
@application.post('/scan')
def upload():

    file = request.files['file']
    filename = file.filename

    if filename == '':
        return jsonify("NULL")

    file_uuid = str(uuid.uuid4())

    # assumes file is svs
    # remove '.svs' from end to get id

    id = filename[:len(filename) - 4]
    ext = 'svs'

    # check if directory exists
    dir_path = DATA_DIR + file_uuid
    path = dir_path

    counter = 1
    while exists(dir_path):
        dir_path = path + "(" + str(counter) + ")"
        counter += 1

    # id = dir_path.split('/')[-1]
    file_path = "{}/{}.{}".format(dir_path,id,ext)

    mkdir(dir_path)

    
    now = datetime.now()

    file_path = save_file(file, id, ext, file_uuid)
    create_meta(str(file_uuid), id, dir_path)

    return jsonify(str(file_uuid))

# delete scan
@application.delete('/scan')
def delete():

    # id = request.args["ids"]

    # dir_path = DATA_DIR + id

    # try:
    #     shutil.rmtree(dir_path)
    #     return jsonify("DONE")
    # except Exception as e:
    #     return jsonify(e)

    # ids = request.args["ids[]"]
    # exts = request.args["extension[]"]
    ids = request.args.getlist('ids[]')
    exts = request.args.getlist("extension[]")
    # ids = request.json["ids[]"]
    # ids = request.json["extension[]"]
    
    meta_file = ''

    for id in ids:
        for ext in exts:

            dir_path = DATA_DIR + id

            if ext == "svs":
                # print(dir_path)
                try:
                    shutil.rmtree(dir_path)
                    # return jsonify("DONE")
                    break
                except Exception as e:
                    
                    return jsonify(e)

            else:
                for f in listdir(dir_path):
                    if f.endswith(ext):

                        remove(join(dir_path, f))
                        meta_file = get_meta(id)
                        meta_path = get_meta(id)

                        with open(meta_path, 'r') as f:
                            data = json.load(f)

                        key = ext + "Status"
                        data[key] = "none"
                        print(key)

                        with open(meta_path, 'w') as json_file:
                            json.dump(data, json_file)

                        break

                # file = dir_path + '/' + id + '.' + ext                
                # if not exists(file):
                #     continue
                # remove(file)
    
    return jsonify("DONE")

@application.put('/scan')
def scan_rename():
    id = request.args["ids"]
    new_name = request.args["new_name"]

    dir_path = DATA_DIR + id

    # meta_file = dir_path + id + ".meta"

    # meta_path = dir_path + '/' + id + '.meta'
    meta_path = get_meta(id)

    with open(meta_path, 'r') as f:
            data = json.load(f)
        
    data["fileName"] = new_name

    with open(meta_path, 'w') as json_file:
        json.dump(data, json_file)

    for f in listdir(dir_path):

        file_name = f.split('.')
        ext = file_name[-1]
        file = new_name + '.' + ext

        rename(dir_path+'/'+f, dir_path+'/'+file)
    
    new_dir = DATA_DIR + new_name
    rename(dir_path, new_dir)
    
    return jsonify("DONE")
    
PNG_EXT="png"
TIF_EXT="tif"
MASK_EXT="mask"
META_EXT="meta"
SVS_EXT="svs"

def make_fpath(uuid, ext):
    return os.path.join(DATA_DIR, uuid, uuid + "." + ext)

def get_svs_dir(uuid):
    return os.path.join(DATA_DIR, uuid, "")

def set_meta_field(uuid, field, value):
    fpath = make_fpath(uuid, META_EXT)
    # print(fpath)
    meta = None
    with open(fpath, "r") as f:
        meta = json.loads(f.read())
        meta[field] = value
    
    if meta:
        with open(fpath, "w") as o:
            json.dump(meta, o)

@celery.task()
def make_png(uuid, svs_fpath, dest):
    set_meta_field(uuid, "pngStatus", "inProgress")
    res = svs_to_png(svs_fpath, dest)
    if res != GOOD:
        set_meta_field(uuid, "pngStatus", str(res))
        return
    set_meta_field(uuid, "pngStatus", "completed")
    return
@celery.task()
def make_tif(uuid, svs_fpath, dest):
    set_meta_field(uuid, "tifStatus", "inProgress")
    res = svs_to_tiff(svs_fpath, dest)
    if res != GOOD:
        set_meta_field(uuid, "tifStatus", str(res))
        return
    set_meta_field(uuid, "tifStatus", "completed")
    return
 
@celery.task()
def make_mask(uuid, svs_fpath, dest):
    time.sleep(60)
    return

TASK_MAP = {
    PNG_EXT: make_png,
    TIF_EXT: make_tif,
    MASK_EXT: make_mask
}


# run algo, generate mask
@application.post('/generate')
def generate():
    print(request.json)
    target_svs = request.json["ids"]
    target_exts = request.json["extension"]
    
    res = {
        "ids": []
    }
    for target in target_svs:
        # target = make_id(target)
        print(target)
        print(get_svs_dir(target))
        if exists(get_svs_dir(target)):
            print("made it")
            res["ids"].append(target)
            for e in target_exts:
                print(make_fpath(target, SVS_EXT))
                print(make_fpath(target, e))
                TASK_MAP[e].delay(target, make_fpath(target, SVS_EXT), make_fpath(target, e))
    return jsonify(res), 200



if __name__ == '__main__':
    print(sys.path)
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not exists(META_DIR):
        os.makedirs(META_DIR)
    application.run(debug=True, port = 8080)

