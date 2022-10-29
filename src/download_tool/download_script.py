import logging
import re
import time
import sys
import os
from Crypto.Hash import MD5


cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))

from gdc_client import gdc_client
from download_tool.download.DownloadError import DownloadError
from download_tool.download.download_error_handler import download_error_handler
from cml.cml_validator import *
from config import *

logger = logging.getLogger("download_tool")

# create console handler with a higher log level
efh = logging.FileHandler('download_error.log')
efh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

efh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(efh)
logger.addHandler(ch)


DELIM = "\t"
I_ID = 0
I_FILENAME = 1
I_MD5_SUM = 2
I_SIZE = 3
I_STATE = 4

SVS_EXTENSION = "svs"
TGCA_PREFIX = "TGCA"
GBM = "GBM"
LGG = "LGG"


def setup_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.path.isfile(path):
        logger.critical("Can't create output directory for downloaded files.")
        exit(os.EX_CANTCREAT)


def setup_progress_log(path):
    if os.path.exists(path) and os.path.isdir(path):
        logger.critical(
            "Cannot create progress log. Path already exists and it is a directory."
        )
        exit(os.EX_CANTCREAT)
    elif not os.path.exists(path):
        with open(path, "a") as f:
            return

def setup_download_failure_log(path):
        if os.path.exists(path) and os.path.isdir(path):
            logger.critical(
                "Cannot create failure log. Path already exists and it is a directory."
            )
            exit(os.EX_CANTCREAT)
        elif not os.path.exists(path):
            with open(path, "a") as f:
                return

if __name__ == "__main__":
    # Read in command line arguments and validate
    cml_validator()

    # Read in config and do some basic validating
    try:
        conf = load_config(sys.argv[I_CML_CONFIG_FILE], v_mandate_fields)
    except (KeyError, FileNotFoundError) as e:
        print(f"Bad config: {repr(e)}", file=sys.stderr)
        exit(os.EX_CONFIG)

    # output directory for downloaded files
    setup_output_dir(conf[OUTPUT_DIR])
    setup_progress_log(conf[PROGRESS_LOG])

    gdc = gdc_client()

    finished = False
    while not finished:
    # skip to line in manifest we are up to
        last_id = ""
        with open(conf[PROGRESS_LOG], "r") as f:
            lns = f.readlines()
            if len(lns) > 0:
                last_id = lns[-1].split(",")[0]
        


        try:
            with open(sys.argv[I_CML_MANIFEST_FILE], "r") as f:
                if last_id:
                    found = False
                    while not found:
                        ln = f.readline()
                        if ln.split(DELIM)[0] == last_id:
                            found = True

                with open(conf[PROGRESS_LOG], "a") as p:
                    for ln in f:
                        ln = ln.strip()
                        logger.info("Manifest line read: %s", ln)
                        sln = ln.split(DELIM)
                        if len(ln) < 3:
                            logger.warning(
                                "Unexpected data format: Split line has length: %s, expected length of 4. Line was: %s",
                                len(sln),
                                ln,
                            )
                            continue

                        try:
                            # output dir
                            out_path = conf[OUTPUT_DIR]

                            #this is false when this script is used for predict_manifest.
                            if conf[MIMIC_GDC_FOLDERS]:
                                # object dir
                                out_path = os.path.join(out_path, sln[I_ID])
                                if not os.path.exists(out_path) and not os.path.isdir(out_path):
                                    print(out_path)
                                    os.mkdir(out_path)

                            out_path =  os.path.join(out_path, sln[I_FILENAME])
                            # download data as a stream to limit RAM usage
                            gdc.stream_download_file(sln[I_ID], sln[I_MD5_SUM], out_path, conf[CHUNK_SIZE])
                            
                            # write the file details to the progress log
                            p.write(sln[I_ID]  + "," + out_path + "\n")
            

                        except DownloadError as e:
                            logger.exception(repr(e))
                            download_error_handler(conf[FAILURE_LOG], ln)
                    
                    finished = True
        except IOError as e:
            logging.critical(f"Can't open critical file. {repr(e)}")
            print(f"Can't open critical file. {repr(e)}", file=sys.stderr)
            exit(os.EX_IOERR)
        
        except Exception as e:
            logging.exception(repr(e))
            time.sleep(120)
            continue

