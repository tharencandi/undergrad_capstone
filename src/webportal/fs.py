import os

from metafiles import *

PNG_EXT="png"
TIF_EXT="tif"
TIFF_EXT="tiff"
MASK_EXT="mask.tif"
META_MASK_KEY="mask"
META_EXT="meta"
SVS_EXT="svs"

def populate_meta(object_dir_path, meta_path):
    object_files = [os.path.join(object_dir_path, f) for f in os.listdir(object_dir_path) if os.path.isfile(os.path.join(object_dir_path, f))]
    fnmask = None
    fnPNG = None
    fnTIF = None
    fnSVS = None


    for f in object_files:
        if f.endswith(PNG_EXT):
            fnPNG = f
            set
        elif f.endswith(MASK_EXT) or f.endswith(META_MASK_KEY):
            fnmask = f
        elif f.endswith(TIF_EXT) or f.endswith(TIFF_EXT):
            fnTIF = f
        elif f.endswith(SVS_EXT):
            fnSVS = f
        else:
            pass
    


class case_centric_fs:
    def __init__(self, base_path):
        self.base_path = base_path
    
    def make_meta_files(self, meta_out_dir):
        if not os.path.exists(self.base_path) and os.path.isdir(self.base_path):
            return
        
        cases = []
        case_dirsp = {}
        for cdir in os.listdir(self.base_path):
            path = os.path.join(self.base_path, cdir)
            if os.path.isdir(path):
                cases.append(cdir)
                case_dirsp[cdir] = path

        for c in cases:
            objects = []
            objectd_paths = {}
            object_dirsp = [ofor o in os.listdir(case_dirsp[c] ) if os.path.isdir(os.path.join(case_dirsp[c] , o))]

            for o in object_dirsp:
                make_meta(uuid, meta_dir, case=c, objectId=o)
                populate_meta(o, get_meta_path(uuid, meta_dir))





    


