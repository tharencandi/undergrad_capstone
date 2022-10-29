import argparse
import sys
import os
from integrity import file_checksum
from download_script import DELIM, I_ID, I_FILENAME, I_MD5_SUM, I_SIZE, I_STATE, SVS_EXTENSION

MANIFEST_HEADER="id	filename	md5	size	state"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to validate the output of the download tool. It will generate a new manifest file of all objects which failed validation so that they may be retried.")
    parser.add_argument('--inputManifestPath', type=str, required=True, help="The manifest file used for the download")
    parser.add_argument('--dataDirPath', type=str, required=True, help="Path to the directory which contains the download tools output. For example, the TGCA_LGG directory in the hardrive.")
    parser.add_argument('--outputManifestDestination', type=str, required=True, help="Path including filename of the output manifest file consisting of all downloads which failed validation")

    args = parser.parse_args()

    outmanifest = args.outputManifestDestination
    inmanifest = args.inputManifestPath
    datadir = args.dataDirPath

    try:
        with open(inmanifest, "r") as im:
            with open(outmanifest, "w") as om:
                #skip header
                im.readline()

                #write header
                om.writelines([MANIFEST_HEADER + "\n"])
                
                for ln in im:
                    ln = ln.strip()
                    lsln = ln.split(DELIM)
                    object_dir = lsln[I_ID]
                    fname = lsln[I_FILENAME]
                    checksum = lsln[I_MD5_SUM]
                    
                    full_fpath = os.path.join(datadir, object_dir, fname)
                    if not file_checksum(full_fpath, checksum):
                        om.writelines(ln + "\n")
    except IOError:
        print("Unable to manifest files.\n", file=sys.stderr)
        exit(1)






