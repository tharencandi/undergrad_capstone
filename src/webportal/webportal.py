from flask import Flask, request, jsonify, send_file, g, render_template, Response
from celery import Celery
import argparse
from os import listdir, mkdir, remove, rename
from os.path import isfile, join, exists, expanduser, getctime, dirname, realpath
from datetime import datetime
import zipfile
import uuid
# from Crypto.Hash import SHA256
import json
import shutil
import sys, os

from meta_files import *
from fs import *

cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))


from image_tools.conversion import svs_to_png, svs_to_tiff
from image_tools.conversion import GOOD
from download_tool.gdc_client import gdc_client
from download_tool.download import *


application = Flask(__name__, static_url_path='',
                  static_folder='frontend/build',
                  template_folder='frontend/build')

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery("webportal", broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)

home = expanduser("~")
WEB_PORTAL_DIR =join(home, ".glioblastoma_portal", "")
DATA_DIR = join(WEB_PORTAL_DIR, "scans/")
DATA_DIR_K = "datadir"
META_DIR_K = "metadir"
dir = dirname(realpath(__file__))
META_DIR = join(WEB_PORTAL_DIR, 'meta_files')
valid_extensions = ["png", "svs", "tif", "tiff", "mask.tiff"]


# get specific file path,
def get_file(uuid, ext, data_dir):
    dir_path = data_dir  + uuid

    name = ''
    for f in listdir(dir_path):
        if f.endswith(ext):

            print(f.endswith('.mask.tif'))
            if ext == ('tif' or 'tiff') and (f.endswith('.mask.tif')or f.endswith('.mask.tiff')):
                print("cont")
                continue
            name = f
            break

    if name == '':
        return ""

    file_path = "{}/{}".format(dir_path,name)

    return file_path


# get meta file, returns path to meta file
def get_meta(uuid, meta_dir):

    meta_path = join(meta_dir, uuid + '.meta')
    if exists(meta_path):
        return meta_path
    else:
        return ""


# save file object into file system
# def save_file(file_obj, id, ext, uuid, data_dir):

#     dir_path = data_dir  + uuid
#     file_path = "{}/{}.{}".format(dir_path,id,ext)

#     file_obj.save(file_path)
#     return file_path

def create_meta(uuid, file_name, case, dir_path, meta_dir):

    meta_path = get_meta_path(uuid, meta_dir)
    file_path = join(dir_path, file_name) + '.svs'
    print(meta_path)
    print(file_path)
    print(uuid)
    print(file_name)
    print(dir_path)

    meta_data = {
        'fileId': uuid,
        'case': case,
        "fileName": file_name,
        "dirPath": dir_path,
        "filePath": file_path,
        "created": "",
        "tifStatus": "none",
        "tifJobId": "",
        "pngStatus": "none",
        "pngJobId": "",
        "maskStatus": "none",
        "maskJobId": "" 
    }


    with open(meta_path, 'w') as json_file:
        json.dump(meta_data, json_file)


# home page
@application.get('/')
def index():
    return render_template("index.html")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@application.get('/all')
def all_scans():
    # check for updates first
    res = {}
    print(application.config[META_DIR_K])
    for f in listdir(application.config[META_DIR_K]):
        meta_json = dict()
        with open(os.path.join(application.config[META_DIR_K], f), "r") as f:
            meta_json = json.load(f)
            res[meta_json["fileId"]] = meta_json


    return jsonify(res)

  


@application.get('/scan')
def get_scan():
    #
    ids = request.args["ids[]"]
    ext = request.args["extension[]"]
    
    fname = get_meta_field(ids, "fileName", application.config[META_DIR_K])
    path = make_fpath(ids, fname, ext, application.config[META_DIR_K])

    if not exists(path):
        abort(404)
    else:
        return send_file(path)

# upload a new scan
@application.post('/scan')
def upload():

    file = request.files['file']
    filename = file.filename

    if filename == '':
        return abort(400)
    
    file_uuid = str(uuid.uuid4())

    object_dir = os.path.join(application.config[DATA_DIR_K], file_uuid)
    if not exists(object_dir):
        mkdir(object_dir)

    base_fname = "".join(filename.split(".")[:-1])
    print(base_fname)
    create_meta(file_uuid, base_fname, case_centric_ftree.UKNOWN_CASE,object_dir, application.config[META_DIR_K])

    save_path = make_fpath(file_uuid, base_fname, SVS_EXT, application.config[META_DIR_K])
    print(save_path)
    file.save(save_path)
    file_create_date = getctime(save_path)
    set_meta_field(file_uuid, "created", datetime.fromtimestamp(file_create_date).strftime('%Y-%m-%d %H:%M:%S'), application.config[META_DIR_K])

    return jsonify(file_uuid)

@application.get("/cancel")
def cancel():
    # for each meta file change everything not completed to none
    for dir in listdir(application.config[DATA_DIR_K] ):
        meta_path = get_meta(dir, application.config[META_DIR_K])

        for e in [PNG_EXT, TIF_EXT, META_MASK_KEY]:
            field = e+"JobId"
            jid = get_meta_field(dir, field, application.config[META_DIR_K])
            if jid != "":
                celery.control.revoke(jid, terminate=True, signal="SIGUSR1")
            set_meta_field(dir, field, "", application.config[META_DIR_K])



    return "", 200

# delete scan
@application.delete('/scan')
def delete():

    ids = request.args.getlist('ids[]')
    exts = request.args.getlist("extension[]")
    # ids = request.json["ids[]"]
    # ids = request.json["extension[]"]
    
    for uuid in ids:
        fname = get_meta_field(uuid, "fileName", application.config[META_DIR_K])
        for ext in exts:
            if ext != SVS_EXT and get_meta_field(uuid, ext + "Status", application.config[META_DIR_K]) == "completed":
                os.remove(make_fpath(uuid, fname, ext, application.config[META_DIR_K]))
                set_meta_field(uuid, ext + "Status", "none", application.config[META_DIR_K])
            elif ext == SVS_EXT:
                shutil.rmtree(get_meta_field(uuid, "dirPath", application.config[META_DIR_K]))
                os.remove(get_meta_path(uuid, application.config[META_DIR_K]))
    
    return "", 200

@application.get('/name')
def scan_rename():
    print(request.args)
    id = request.args["ids"]
    new_name = request.args["new_name"]

    dir_path = get_meta_field(id, "dirPath", application.config[META_DIR_K])
    set_meta_field(id, "fileName", new_name, application.config[META_DIR_K])

    for f in listdir(dir_path):

        ext = f.split(".")
        os.rename(os.path.join(dir_path, f), os.path.join(dir_path, new_name + "." + ext))

    return "", 200
    


@celery.task()
def make_png(uuid, svs_fpath, dest, meta_dir):
    set_meta_field(uuid, "pngStatus", "inProgress", meta_dir)
    res = svs_to_png(svs_fpath, dest)
    if res != GOOD:
        set_meta_field(uuid, "pngStatus", "failed", meta_dir)
        return
    set_meta_field(uuid, "pngStatus", "completed", meta_dir)
    return

@celery.task()
def make_tif(uuid, svs_fpath, dest, meta_dir):
    set_meta_field(uuid, "tifStatus", "inProgress", meta_dir)
    res = svs_to_tiff(svs_fpath, dest)
    if res != GOOD:
        set_meta_field(uuid, "tifStatus", "failed", meta_dir)
        return
    set_meta_field(uuid, "tifStatus", "completed", meta_dir)
    return
 
@celery.task()
def make_mask(uuid, svs_fpath, dest, meta_dir):
    time.sleep(60)
    return

@celery.task()
def download_from_manifest(manifest):
    pass
TASK_MAP = {
    PNG_EXT: make_png,
    TIF_EXT: make_tif,
    MASK_EXT: make_mask
}

@application.post('/automateddownload')
def download_gdc_files():
    if not request.files or 'file' not in request.files:
        return "", 400
    file = request.files['file']
    fname = file.filename

    manifest = file.read()

    return "", 200

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
        if exists(get_svs_dir(target, application.config[META_DIR_K])):
            fname = get_meta_field(target, "fileName", application.config[META_DIR_K])
            res["ids"].append(target)
            for e in target_exts:
                task = TASK_MAP[e].delay(target, make_fpath(target, fname , SVS_EXT, application.config[META_DIR_K]), make_fpath(target, fname , e, application.config[META_DIR_K]), application.config[META_DIR_K])
                set_meta_field(target, e + "JobId", task.id, application.config[META_DIR_K])
        else:
            pass

    return jsonify(res), 200

HELP="Absolute path to an existing directory of wholside data. It expects the directory to consist of a set of sub directories representing each case, with each wholeslide object stored in its own sub directory within the directory of the case to which it belongs."

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Glioblastoma processing portal. ')
    parser.add_argument('--existingDataPath', help=HELP)
    args = parser.parse_args()
    print(args)
    application.config[DATA_DIR_K] = DATA_DIR
    application.config[META_DIR_K] = META_DIR

    if args.existingDataPath is not None:
        print(args)
        print(args)
        application.config[META_DIR_K] = os.path.join(args.existingDataPath, ".meta")
        if not os.path.exists(application.config[META_DIR_K]):
            os.makedirs(application.config[META_DIR_K])
        data_tree = case_centric_ftree(args.existingDataPath)
        data_tree.make_meta_files_if_not_exist(application.config[META_DIR_K])
        application.config[DATA_DIR_K]  = os.path.join(data_tree.get_case_dir(case_centric_ftree.UKNOWN_CASE))


    if not os.path.exists(application.config[DATA_DIR_K] ):
        os.makedirs(application.config[DATA_DIR_K] )
    if not os.path.exists(application.config[META_DIR_K]):
            os.makedirs(application.config[META_DIR_K])
    application.run(debug=True, port = 8080)

