import sys
import os

CML_ERR_MSG = """
Usage:\n
python3 download_script.py [manifest file path] [tool configuration file path] <start:end>

start and end must be positive integers. They represent the range of entries in the manifest file to download.
"""
COMPULSORY_ARGS_LEN=3

I_CML_MANIFEST_FILE = 1
I_CML_CONFIG_FILE = 2
I_CML_DOWNLOAD_RANGE=3
def cml_validator():
    if len(sys.argv) < COMPULSORY_ARGS_LEN:
        print(CML_ERR_MSG, file=sys.stderr)
        exit(os.EX_USAGE)
    if len(sys.argv) == COMPULSORY_ARGS_LEN + 1:
        validate_download_range()

def validate_download_range():
    drange = sys.argv[I_CML_DOWNLOAD_RANGE]
    drange = drange.split(":")
    if len(drange)  != 2:
        print("Invalid download range.\n\n" + CML_ERR_MSG, file=sys.stderr)
        exit(os.EX_USAGE)
    
    for i in drange:
        try:
            i = int(i)
            if not i > 0:
                raise ValueError()
        except ValueError:
            print("Invalid download range. Must be positive integers\n\n" + CML_ERR_MSG, file=sys.stderr)
            exit(os.EX_USAGE)
