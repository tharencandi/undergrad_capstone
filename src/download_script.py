import json, requests, logging, re, sys, os
from Crypto.Hash import MD5
from download.gdc_client import gdc_client
from download.DownloadError import DownloadError

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
OUT_DIR_PATH = "../downloaded_data"
PROGRESS_FILE_PATH= "../progress.txt"

I_CML_MANIFEST=1
CML_MSG="""
Usage:\n
python3 download_script.py [manifest file path]
"""
def has_file_ext(fname, ext):
    r = re.compile("[\S]+\." + ext + "$")
    return r.match(fname)

def create_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.path.isfile(path):
        logging.critical("Can't create output directory for downloaded files.")
        print("Can't create output_dir", file=sys.stderr)
        exit(os.EX_CANTCREAT)

def create_progress_file(path):
    if os.path.exists(path) and os.path.isdir(path):
        logging.critical("Cannot create progress file. Path already exists and it is a directory.")
        print("Can't create progress file.", file=sys.stderr)
        exit(os.EX_CANTCREAT)
    elif not os.path.exists(path):
        with open(path, "a") as f:
            return


def cml():
    if len(sys.argv) < 2:
        print(CML_MSG, file=sys.stderr)
        exit(os.EX_USAGE)

if __name__ == "__main__":
    cml()
    create_output_dir(OUT_DIR_PATH)
    create_progress_file(PROGRESS_FILE_PATH)
    gdc = gdc_client()
    with open(sys.argv[I_CML_MANIFEST], "r") as f:
        with open(PROGRESS_FILE_PATH, "a") as p:
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
                    out_path = OUT_DIR_PATH + "/" +  sln[I_FILENAME]
                    gdc.download_file(sln[I_ID], sln[I_MD5_SUM], out_path)
                    p.write(sln[I_ID] + "\t" + out_path + "\t" + sln[I_MD5_SUM] + "\n")
                except DownloadError as e:
                    logging.warning("Download failed with reason: %s", e.reason)
                    download_error_handler(ln, e.reason)
