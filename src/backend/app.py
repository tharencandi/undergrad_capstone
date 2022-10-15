from flask import Flask, request, jsonify, send_file
from os import listdir, mkdir, remove
from os.path import isfile, join, exists
from datetime import datetime
import zipfile
import threading


# placeholder for algo
def generate_mask():
    print("mask function")
    return

app = Flask(__name__)

# scan_path = "../../scans/"
scan_path = "./scans/"
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

# download specified scan as extension as zipped file
@app.get('/scan')
def get_scan():
    # TODO
    ids = request.args["ids"]
    ext = request.args["extension"]

    filenames = []
    ids = ids.split(',')
    ext = ext.split(',')
    
    # for id in ids:
    for i in range(0, len(ids)):

        # check if directory exists, create if not
        dir_path = scan_path + ids[i]
        file_path = "{}/{}.{}".format(dir_path,ids[i],ext[i])

        if not exists(file_path):
            return jsonify("File not Found: "+ file_path)
        
        else:
            filenames.append(file_path)

    with zipfile.ZipFile("multiple_files.zip", mode="w") as archive:
        for filename in filenames:

            archive.write(filename)
    
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
    file_path = "{}/{}.{}".format(dir_path,id,ext)
    
    if not exists(dir_path):
        mkdir(dir_path)
    
    # check if file exists
    if exists(file_path):
        return jsonify("file already exists")

    # create file
    file.save(file_path)

    f = open("{}/{}.meta".format(dir_path,id), "w")

    now = datetime.now()
    f.write(now.strftime("%d/%m/%Y %H:%M:%S"))

    f.close()



    return jsonify("DONE")

# delete scan
@app.delete('/scan')
def delete():

    ids = request.args["ids"]
    ext = request.args["extension"]

    dir_path = scan_path + ids
    file_path = "{}/{}.{}".format(dir_path,ids,ext)

    if exists(file_path):
        remove(file_path)
        return jsonify("DONE")

    else:
        return jsonify("error")
    
    

# run algo, 
@app.get('/scan/generate')
def generate():
    generate_mask() #placeholder



if __name__ == '__main__':
	app.run(debug=True)

