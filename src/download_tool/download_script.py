import logging
import re
import sys
import os
from Crypto.Hash import MD5
from download.gdc_client import gdc_client
from download.DownloadError import DownloadError
from cml.cml_validator import *
from config import *

logging.basicConfig(level=logging.DEBUG)

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

# DL_CHUNK_SIZE=8192





# def has_file_ext(fname, ext):
#     r = re.compile("[\S]+\." + ext + "$")
#     return r.match(fname)


def setup_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.path.isfile(path):
        logging.critical("Can't create output directory for downloaded files.")
        print("Can't create output_dir", file=sys.stderr)
        exit(os.EX_CANTCREAT)


def setup_progress_log(path):
    if os.path.exists(path) and os.path.isdir(path):
        logging.critical(
            "Cannot create progress log. Path already exists and it is a directory."
        )
        print("Can't create progress log.", file=sys.stderr)
        exit(os.EX_CANTCREAT)
    elif not os.path.exists(path):
        with open(path, "a") as f:
            return

def setup_download_failure_log(path):
        if os.path.exists(path) and os.path.isdir(path):
            logging.critical(
                "Cannot create failure log. Path already exists and it is a directory."
            )
            print("Can't create failure log.", file=sys.stderr)
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

    # Setup logging, output directory for downloaded files, progress and failure logs
    logging.basicConfig(filename=conf[LOGFILE], level=conf[LOGLEVEL])
    setup_output_dir(conf[OUTPUT_DIR])
    setup_progress_log(conf[PROGRESS_LOG])
    setup_download_failure_log(conf[FAILURE_LOG])

    gdc = gdc_client()
    with open(sys.argv[I_CML_MANIFEST_FILE], "r") as f:
        with open(conf[PROGRESS_LOG], "a") as p:
            for ln in f:
                ln = f.readline().strip()
                logging.info("Manifest line read: %s", ln)
                sln = ln.split(DELIM)
                if len(ln) < 3:
                    logging.warning(
                        "Unexpected data format: Split line has length: %s, expected length of 4. Line was: %s",
                        len(sln),
                        ln,
                    )
                    continue

                try:
                    # create an output path for the downloaded data
                    out_path = conf[OUTPUT_DIR] + "/" + sln[I_FILENAME]

                    # download data as a stream to limit RAM usage
                    gdc.stream_download_file(sln[I_ID], sln[I_MD5_SUM], out_path, conf[CHUNK_SIZE])
                    
                    # write the file details to the progress log
                    p.write(sln[I_ID] + "\t" + out_path + "\t" + sln[I_MD5_SUM] + "\n")

                except DownloadError as e:
                    logging.warning("Download failed with reason: %s", e.reason)
                    # log the origin line from the manifest and the reason to failure log
                    download_error_handler(conf[FAILURE_LOG], ln, repr(e))

