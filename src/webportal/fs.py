import os

from metafiles import *

PNG_EXT="png"
TIF_EXT="tif"
TIFF_EXT="tiff"
MASK_EXT="mask.tif"
META_MASK_KEY="mask"
META_EXT="meta"
SVS_EXT="svs"

def populate_meta(uuid, object, case, object_dir_path, meta_dir):
    object_files = [os.path.join(object_dir_path, f) for f in os.listdir(object_dir_path) if os.path.isfile(os.path.join(object_dir_path, f))]
    fnmask = None
    fnPNG = None
    fnTIF = None
    fnSVS = None


    for f in object_files:
        if f.endswith(PNG_EXT):
            fnPNG = f
            set_meta_field(uuid, "pngStatus", "completed", meta_dir)
        elif f.endswith(MASK_EXT) or f.endswith(META_MASK_KEY):
            fnmask = f
            set_meta_field(uuid, " maskStatus", "completed", meta_dir)
        elif f.endswith(TIF_EXT) or f.endswith(TIFF_EXT):
            fnTIF = f
            set_meta_field(uuid, "tifStatus", "completed", meta_dir)
        elif f.endswith(SVS_EXT):
            fnSVS = f
            set_meta_field(uuid, "filePath", os.path.join(object_dir_path, f), meta_dir)
            set_meta_field(uuid, "fileName", f[:len(f)-4], meta_dir)
        else:
            pass
    


class case_centric_ftree:
    UKNOWN_CASE = "webportal_default_case"

    def __init__(self, base_path):
        if not os.path.exists(self.base_path) and os.path.isdir(self.base_path):
            raise ValueError(f"{base_path} is not a direcctory.")
        self.base_path = base_path
        self.cases = self.find_existing_cases()
    
    def find_existing_cases(self):
        cases = []
        case_dirsp = {}
        for cdir in os.listdir(self.base_path):
            if os.path.isdir(path):
                cases.append(cdir)
        if not os.path.exists(os.path.join(self.base_path, case_centric_fs.UKNOWN_CASE)):
            os.mkdir(os.path.join(self.base_path, case_centric_fs.UKNOWN_CASE))
        cases.append(case_centric_fs.UKNOWN_CASE)

    def get_case_dir(self, case):
        if case in cases:
            return os.path.join(self.base_path, cdir)
        else:
            raise ValueError("Not a known case.")

    def get_object_dir(self, case, object_uuid):
        return os.join(self.get_case_dir(case), object_uuid)

    def make_meta_files_if_not_exist(self, meta_out_dir):
        for c in self.cases:
            objects = [o for o in os.listdir(self.get_case_dir(c) ) if os.path.isdir(self.get_object_dir(c, o))]

            for o in objects:
                meta_path = get_meta_path(o, meta_out_dir)
                if not os.path.exists(meta_path):
                    make_meta(uuid, meta_dir, case=c, fileId=o, dirPath=self.get_object_dir(c, o))
                    populate_meta(o, meta_path)





    


