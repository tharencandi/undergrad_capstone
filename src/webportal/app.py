from flask import Flask, request, jsonify, send_file, g, render_template
import sqlite3
from celery import Celery
from os import listdir, mkdir, remove, rename
from os.path import isfile, join, exists
from datetime import datetime
import zipfile
import uuid
import json
import shutil
# from conversion import svs_to_png, svs_to_tiff


app = Flask(__name__, static_url_path='',
                  static_folder='frontend/build',
                  template_folder='frontend/build')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

scan_path = "./scans/"
valid_extensions = ["png", "svs", "tif"]

WEB_PORTAL_DIR="temp"
DATABASE = 'temp/file.db'

# for testing
# WEB_PORTAL_DIR = "/home/"
# DATABASE = '/home/'


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
  
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db_if_not_exists():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read()) 
        db.commit()

# get specific file path,
def get_file(name, ext):
    dir_path = WEB_PORTAL_DIR + name
    file_path = "{}/{}.{}".format(dir_path,name ,ext)

    return file_path

# get meta file, returns path to meta file
def get_meta(id):
    meta_path = WEB_PORTAL_DIR+ id + '/' + id + ".meta"
    return meta_path

# save file object into file system
def save_file(file_obj, id, ext):

    dir_path = WEB_PORTAL_DIR + id
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
    return jsonify(WEB_PORTAL_DIR)

# home page
@app.get('/')
def index():
    return render_template("index.html")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@app.get('/all')
def all_scans():
    scans = [f for f in listdir(WEB_PORTAL_DIR) if not isfile(join(WEB_PORTAL_DIR, f))]
    
    scan_list = []
    # return jsonify("a1")
    for id in scans:
        scan_id = id
        extensions = []
        date = ""
        dir_path = "{}{}/".format(WEB_PORTAL_DIR,id)

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
    dir_path = join(WEB_PORTAL_DIR, ids)
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

    # assumes file is svs
    # remove '.svs' from end to get id
    id = filename[:len(filename) - 4]
    ext = 'svs'

    # check if directory exists
    dir_path = WEB_PORTAL_DIR + id
    path = dir_path

    counter = 1
    while exists(dir_path):
        dir_path = path + "(" + str(counter) + ")"
        counter += 1

    id = dir_path.split('/')[-1]
    file_path = "{}/{}.{}".format(dir_path,id,ext)
    
    mkdir(dir_path)

    file_uuid = uuid.uuid4()
    now = datetime.now()
    
    meta_data = {
        'fileId': str(file_uuid),
        "fileName": filename,
        "created": now.strftime("%d/%m/%Y %H:%M:%S"),
        "tifStatus": "none",
        "pngStatus": "none",
        "maskStatus": "none",
        "downloadStatus": "none"
    }

    with open("{}/{}.meta".format(dir_path,id), 'w') as json_file:
        json.dump(meta_data, json_file)

    save_file(file, id, ext)
    return jsonify(str(file_uuid))

# delete scan
@app.delete('/scan')
def delete():

    # ids = request.args.getlist("ids")
    id = request.args["ids"]

    dir_path = WEB_PORTAL_DIR + id

    try:
        shutil.rmtree(dir_path)
        return jsonify("DONE")
    except Exception as e:
        return jsonify(e)

@app.put('/scan')
def scan_rename():
    id = request.args["ids"]
    new_name = request.args["new_name"]

    dir_path = WEB_PORTAL_DIR + id

    # meta_file = dir_path + id + ".meta"
    meta_path = dir_path + '/' + id + '.meta'

    with open(meta_path, 'r') as f:
            data = json.load(f)
        
    data["fileName"] = new_name

    with open(meta_path, 'w') as json_file:
        json.dump(data, json_file)

    for f in listdir(dir_path):

        file_name = f.split('.')

        file_name[0] = new_name
        file = file_name[0] + '.' + file_name[1]

        rename(dir_path+'/'+f, dir_path+'/'+file)
    
    new_dir = WEB_PORTAL_DIR + new_name
    rename(dir_path, new_dir)
    
    return jsonify("DONE")

#######################################################
# un-comment import conversion

# #convert to different format
# @app.get('/scan/convert')
# def convert():
#     id = request.args["ids"]
#     ext = request.args["ext"]

#     # change status file
#     dir_path = WEB_PORTAL_DIR + id
#     meta_path = dir_path + '/' + id + '.meta'

#     with open(meta_path, 'r') as f:
#         data = json.load(f)
    
#     key = ext + "Status"
#     data[key] = "inProgress"
#     with open(meta_path, 'w') as json_file:
#         json.dump(data, json_file)

#     input_file = dir_path + '/' + id + '.svs'


#     # convert
#     if ext == 'png':
#         output_file = dir_path + '/' + id + '.png'
#         svs_to_png(input_file, output_file)

#     elif ext == 'tif':
#         output_file = dir_path + '/' + id + '.tif'
#         svs_to_tiff(input_file, output_file)

#     with open(meta_path, 'r') as f:
#         data = json.load(f)
    
#     data[key] = "Completed"
#     with open(meta_path, 'w') as json_file:
#         json.dump(data, json_file)
# 
#     return jsonify("DONE")
    
###########################################################
    
@celery.task(bind=True)
def generate_mask(self, svs_fpath, mask_dest):
    time.sleep(60)
    return

# run algo, generate mask
@app.post('/scan/mask/generate')
def generate():
    target_svs = request.json["targets"]
    
    res = {
        "tasks" : [
            {

            }
        ]
    }

    for target in target_svs:
        task = generate_mask.delay(target, target + ".mask")
        res["tasks"].append({
            "target": target,
            "task_id": None
        })
    
    return jsonify(res)

@app.get('/task/<task_id>/status')
def taskstatus(task_id):
    pass



if __name__ == '__main__':
    if not exists(WEB_PORTAL_DIR):
        mkdir(WEB_PORTAL_DIR)
    init_db_if_not_exists()
    app.run(debug=True)

