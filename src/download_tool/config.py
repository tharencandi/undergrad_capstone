import os
from yaml import safe_load


OUTPUT_DIR="OUTPUT_DIR"
PROGRESS_LOG="PROGRESS_LOG"
FAILURE_LOG="FAILURE_LOG"
CHUNK_SIZE="CHUNK_SIZE"
CONCURRENT_DOWNLOADS="CONCURRENT_DOWNLOADS"
LOGFILE="LOGFILE"
LOGLEVEL="LOGLEVEL"

MAND_FIELDS = [
    OUTPUT_DIR,
    PROGRESS_LOG,
    FAILURE_LOG,
    CHUNK_SIZE,
    CONCURRENT_DOWNLOADS,
    LOGFILE,
    LOGLEVEL
]

def field_validator(config, *mandated_fields):
    for f in mandated_fields:
        if f not in config:
            raise KeyError(f"Field {f} is compulsory.")

def v_mandate_fields(conf):
    field_validator(conf, *MAND_FIELDS) 

def load_config(config_path, *validators):
    if not os.path.exists(config_path) or not os.path.isfile(config_path):
        raise FileNotFoundError("Config file does not exists.")

    conf = {}
    with open(config_path, "r") as conf:
        conf =  safe_load(conf)
        for v in validators:
            v(conf)

    return conf

