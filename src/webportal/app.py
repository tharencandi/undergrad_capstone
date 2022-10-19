import sys

sys.path.append("/home/haeata/glioblastoma_processing/src/")
print(sys.path)
from flask import Flask, request, jsonify, send_file, g, render_template, abort
import sqlite3
from celery import Celery
from os import listdir, mkdir, remove, rename
from os.path import isfile, join, exists
from datetime import datetime
import zipfile
import uuid
import json
import shutil
from CNN import predict
# from conversion import svs_to_png, svs_to_tiff


app = Flask(__name__, static_url_path='',
                  static_folder='frontend/build',
                  template_folder='frontend/build')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# scan_path = "../../scans/"
scan_path = "./scans/"
valid_extensions = ["png", "svs", "tif"]

MASKING_TEMP_DIR="/home/haeata/..glioblastoma_portal/"
WEB_PORTAL_DIR="/home/haeata/.glioblastoma_portal/"
MASKING_TEMP_DIR=WEB_PORTAL_DIR + ".mask_tmp/"
DATABASE = '/home/haeata/.glioblastoma_portal/file.db' 

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

# home page
@app.get('/')
def index():
    return render_template("index.html")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@app.get('/all')
def all_scans():
    scans = [f for f in listdir(scan_path) if not isfile(join(scan_path, f))]
    
    scan_list = []
    # return jsonify("a1")
    for id in scans:
        scan_id = id
        extensions = []
        date = ""
        dir_path = "{}{}/".format(scan_path,id)

        # get extensions
        files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

        for file in files:
            ext = file[-3:]
            if ext in valid_extensions:
                extensions.append(ext)

        # get date
        meta = scan_path + id + "/" + ".meta"
        meta = "{}{}/{}.meta".format(scan_path, id, id)
        meta_data = open(meta, "r")
        # date = meta_data.readline()
        data = json.load(meta_data)

        meta_data.close()
        # scan_list.append((scan_id, extensions, date))
        scan_list.append(data)
    # return jsonify("a")
    
    return jsonify(scan_list)

# download specified scan as extension as zipped file
@app.get('/scan')
def get_scan():
    #
    ids = request.args.getlist("ids")
    ext = request.args.getlist("extension")

    filenames = []
    files = []
    # ids = ids.split(',')
    # ext = ext.split(',')
    
    # for id in ids:
    for i in range(0, len(ids)):

        # check if directory exists, create if not
        dir_path = scan_path + ids[i]
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
        
        key = ext[i] + "Status"
        data[key] = "Completed"

        with open(meta_path, 'w') as json_file:
            json.dump(data, json_file)
    

    
    return send_file("multiple_files.zip")


# upload a new scan
@app.post('/scan')
def upload():

    file = request.files['file']
    filename = file.filename

    if filename == '':
        return jsonify("NULL")

    id = filename.split(".")[0]
    ext = filename.split(".")[1]

    if ext not in valid_extensions:
        return jsonify("INVALID FILE FORMAT: {}".format(ext))

    # check if directory exists
    dir_path = scan_path + id
    path = dir_path

    counter = 1
    while exists(dir_path):
        print(dir_path)
        dir_path = path + "(" + str(counter) + ")"
        counter += 1

    print("w {}".format(dir_path))
    id = dir_path.split('/')[-1]
    file_path = "{}/{}.{}".format(dir_path,id,ext)
    
    mkdir(dir_path)

    file_id = uuid.uuid4()
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

    with open("{}/{}.meta".format(dir_path,id), 'w') as json_file:
        json.dump(meta_data, json_file)

    print("file: {}".format(file_path))
    file.save(file_path)

    return jsonify("DONE")

# delete scan
@app.delete('/scan')
def delete():

    ids = request.args.getlist("ids")
    # ext = request.args["extension"]
    # print(ids)
    for id in ids:

        dir_path = scan_path + id
        # file_path = "{}/{}.{}".format(dir_path,ids,ext)

        try:
            shutil.rmtree(dir_path)
            return jsonify("DONE")
        except Exception as e:
            return jsonify(e)

@app.put('/scan')
def scan_rename():
    ids = request.args.getlist("ids")
    new_name = request.args["new_name"]

    for id in ids:
        dir_path = scan_path + id

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
        
        new_dir = scan_path + new_name
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
#     dir_path = scan_path + id
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
def generate_mask(self, uuid, svs_fpath, mask_fname):
    out_path = predict.predict_slide(uuid, svs_fpath, svs_dir, MASKING_TEMP_DIR, masks_dir)
    time.sleep(60)
    return {"slide_uuid": uuid,  "fpath":  out_path,  "ftype": ".mask"}

@celery.task(bind=True)
def convert_to_tif(self, svs_fpath, tif_dest):
    time.sleep(60)
    return

@celery.task(bind=True)
def convert_to_png(self, svs_fpath, png_dest):
    time.sleep(60)
    return 

GENERATOR_MAP = {
    ".png" : convert_to_png,
    ".tif": convert_to_tif,
    ".mask": generate_mask
}

ACTION_RES_EXTENSTIONS = {
    ".png" : ".png",
    ".tif": ".tif",
    ".mask": ".mask"
}

def celery_task_to_json(task):
    return {
        "task_id": task.id
    }


INSERT_TASK="INSERT INTO tasks(task_id, task_type, slide_uuid) VALUES(?, ?, ?)"
INSERT_OBJECT="INSERT INTO objects(slide_uuid, fpath, file_type) VALUES(?, ?, ?)"
SELECT_SPECIFIC_TASK="SELECT * FROM tasks where task_id =  (?)"
SELECT_SPECIFIC_WHOLESLIDE="SELECT * FROM wholeslides WHERE uuid = (?)"

def handle_async_success(action, slide_uuid, task):
    status = task.status
    fname = task.get()
    query_db(INSERT_OBJECT, (slide_uuid, fname, action))

# run algo, generate mask
@app.post('/scan/mask/generate')
def generate():
    # retrieve list of svs object ids
    target_svs = request.json["targets"]
    actions = request.json["actions"]

    res = {
        "objects": []
    }

    for target in target_svs:
        # skip jobs for obejcts that don't exist
        if not len(query_db(query, (target))) > 0:
            continue
        object_jobs = {
            "uuid": target
        }
        for action in actions:
            try:
                task = GENERATOR_MAP[action].delay(target, target + ACTION_RES_EXTENSTIONS[action])
                query_db(INSERT_TASK, (task.id, action, target))
                object_jobs[action] = celery_task_to_json(task)
            except KeyError:
                abort(400)

    return jsonify(res)

@app.get('/taskstatus/<task_id>')
def taskstatus(task_id):
    db_res = query_db(SELECT_SPECIFIC_TASK, (task_id))
    if not len(db_res) > 0:
        return 404
    
    reg_task = db_res[0]
    task = GENERATOR_MAP[reg_task["task_type"]].AsyncResult(reg_task["task_id"])
    res = {
        "state": task.status,
    }

    if task.state == "SUCCESS":
        handle_async_success(reg_task["task_type"], reg_task["slide_uuid"], task)
    



if __name__ == '__main__':
    if not exists(WEB_PORTAL_DIR):
        mkdir(WEB_PORTAL_DIR)
    if not exists(MASKING_TEMP_DIR):
        mkdir(MASKING_TEMP_DIR)

    init_db_if_not_exists()
    app.run(debug=True)

