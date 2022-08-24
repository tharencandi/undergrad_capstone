import json, requests, logging, re, sys
from Crypto.Hash import MD5
from gdc_client import gdc_client

DELIM="\t"
I_ID=0
I_FILENAME=1
I_MD5_SUM=2
I_SIZE=3
I_STATE=4

SVS_EXTENSION="svs"

TGCA_PREFIX="TGCA"
GBM="GBM"
LGG="LGG"

def has_file_ext(fname, ext):
    r = re.compile("[\S]*\."+ext+"$")
    return r.match(fname)


ids = []
sums = []
with open(sys.argv[1], "r") as f:
    for ln in f:
        ln = f.readline().strip().split(DELIM)
        if len(ln) <=2:
            logging.warning("Unexpected data format: Split line has length: %s ", len(ln))
            continue
        ids.append(ln[I_ID])
        sums.append(ln[I_MD5_SUM])
        break


gdcc = gdc_client()
gdcc.download_files(ids, sums)




