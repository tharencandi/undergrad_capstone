import os
from case import GBM, LGG
from app import DATA_DIR
from flask import current_app

CASE_DATA_DIR={
    GBM: "TCGA_GBM",
    LGG: "TCGA_LGG"
}

def uuid_dir_exists(case, uuid):
    path = os.path.join(current_app.config[DATA_DIR], CASE_DATA_DIR[case], uuid)
    if not os.path.isdir(path):
        return False
    
    return True

def write_uuid_f(case, uuid, flask_f_object, fname):
    
    uuid_dir = os.path.join(current_app.config[DATA_DIR], CASE_DATA_DIR[case], uuid)
    current_app.logger.info(f"uuid_dir: {uuid_dir}")
    if not os.path.isdir(uuid_dir):
        os.mkdir(uuid_dir)
    
    path = os.path.join(uuid_dir, fname)
    flask_f_object.save(path)
    current_app.logger.info(f"Mask received and written to path: {path}")
    

def uuid_object_exists(case, uuid, fname):
    path = os.path.join(current_app.config[DATA_DIR], CASE_DATA_DIR[case], uuid, fname)
    if os.path.exists(path):
        return True
    return False