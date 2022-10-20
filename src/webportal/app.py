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

# scan_path = "../../scans/"
scan_path = "./scans/"
valid_extensions = ["png", "svs", "tif"]

WEB_PORTAL_DIR="/home/haeata/.glioblastoma_portal/"
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
    



@celery.task()
def make_png(self, svs_fpath, dest):
    time.sleep(60)
    return
@celery.task()
def make_tif(self, svs_fpath, dest):
    time.sleep(60)
    return
@celery.task()
def make_mask(self, svs_fpath, dest):
    time.sleep(60)
    return
TASK_MAP = {
    ".png": make_png,
    ".tif": make_tif,
    ".mask": make_mask
}

def make_fpath(uuid, ext):
    return ""

def get_fpath(uuid, ext):
    return  ""

def set_meta_field(uuid, field, value):
    return ""
# run algo, generate mask
@app.post('/generate')
def generate():
    target_svs = request.json["ids"]
    target_exts = request.json["exts"]

    for target in target_svs:
        for e in target_exts:
            TASK_MAP[e].delay(get_fpath(target, e), make_fpath(target, e))
    return jsonify(res)



if __name__ == '__main__':
    if not exists(WEB_PORTAL_DIR):
        mkdir(WEB_PORTAL_DIR)
    app.run(debug=True)

