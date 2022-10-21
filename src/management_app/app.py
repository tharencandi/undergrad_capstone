
from flask import Flask, jsonify, request, abort
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
import logging

from case import GBM, LGG
from fs import *

logging.basicConfig(filename='management_server.log', level=logging.INFO, format=f'[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = Flask(__name__)

MASK_EXT = ".mask"
DATA_DIR="DATA_DIR"
app.errorhandler(HTTPException)
def api_error(e):
    return jsonify(message=str(e)), e.code

@app.post("/<string:case>/<uuid>/svs")
def receive_svs(case, uuid):
    print("svs")

@app.post("/<string:case>/<uuid>/mask")
def receive_mask(case, uuid):
    app.logger.info(f"Mask posted with case {case}, {uuid}")
    if not (case == GBM or case == LGG):
        app.logger.warning("Not a valid case")
        abort(404)
    
    fname = secure_filename(uuid+MASK_EXT)
    if uuid_object_exists(case, uuid, fname):
        app.logger.warning(f"Object already exists. case: {case}, uuid: {uuid}, fname: {fname}")
        abort(409)
    
    if "file" not in request.files:
        app.logger.debug(request.files)
        app.logger.warning(f"No file given. case: {case}, uuid: {uuid}, fname: {fname}")
        abort(400)
    
    file = request.files["file"]
    try:
        app.logger.info(f"Writing data. case: {case}, uuid:{uuid}, fname:{fname}")
        write_uuid_f(case, uuid, file, fname)
    except IOError as e:
        app.logger.exception(f"IOError {str(e)} when saving mask. case:{case}, uuid:{uuid}, fname:{fname}")
        abort(500)
        
    return "", 200

@app.post("/<string:case>/<uuid>/annotation")
def receive_annotation(case, uuid):
    print("annotation")

if __name__=="__main__":
    # app.run(host="0.0.0.0")
    data_dir = sys.argv[1]
    app.config[DATA_DIR] = data_dir
    app.run(host="localhost", debug=True)
