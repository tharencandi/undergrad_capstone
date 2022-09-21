from flask import Flask, request, jsonify, send_file
from os import listdir, mkdir
from os.path import isfile, join, exists
from datetime import datetime


app = Flask(__name__)

scan_path = "../../scans/"
valid_extensions = ["png", "svs", "tiff"]

# home page
@app.get('/')
def index():
    return jsonify("hello world")

# get all files
# return list of tuples -> (file_id, [extensions], date created)
@app.get('/all')
def all_scans():
    scans = [f for f in listdir(scan_path) if not isfile(join(scan_path, f))]
    
    scan_list = []
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
        date = meta_data.readline()
        meta_data.close()
        scan_list.append((scan_id, extensions, date))
    
    return jsonify(scan_list)

# get specified scan as extension 
@app.get('/scan')
def get_scan():
    # TODO
    id = request.args["id"]
    ext = request.args["extension"]

    # check if directory exists, create if not
    dir_path = scan_path + id
    file_path = "{}/{}.{}".format(dir_path,id,ext)

    # print(file_path)
    if not exists(file_path):
        return jsonify("File not Found")
    
    else:
        # print("found")
        return send_file(file_path)


# create a new scan as extension <ext>
@app.post('/scan/<ext>')
def post_scan(ext):

    # check if directory exists
    dir_path = scan_path + id
    file_path = "{}/{}.{}".format(dir_path,id,ext)
    
    if not exists(dir_path):
        mkdir(dir_path)
    
    # check if file exists
    if exists(file_path):
        return jsonify("file already exists")

    # create file
    
    return jsonify("TODO")


if __name__ == '__main__':
	app.run(debug=True)

