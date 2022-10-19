import os

class MANIFEST_FORMAT_EXCEPTION(Exception):
    DEFAULT_MSG = "data in manifest file is the incorrect format"
    def __init__(self, message):
        if not message:
            message = MANIFEST_FORMAT_EXCEPTION.DEFAULT_MSG
        super().__init__(message)

TMP_DIR = "TMP_DIR"
MANIFEST_IN = "MANIFEST_IN"
MANIFEST_OUT = "MANIFEST_OUT"
MASK_DIR = "MASK_DIR"
SVS_DIR =  "SVS_DIR"
UPLOAD_LOG = "UPLOAD_LOG"
KEYS = [TMP_DIR, MANIFEST_IN, MANIFEST_OUT, MASK_DIR, SVS_DIR, UPLOAD_LOG]
MANIFEST_HEADERS = "id\tfilename\tmd5\tsize\tstate\n"

def clear_dir(dir):
    for file in os.listdir(dir):
        if os.path.isfile(f"{dir}/{file}"):
            os.remove(f"{dir}/{file}")
        else:
            folder = file
            clear_dir(f"{dir}/{folder}")

def conf_init(conf):
        for key in conf:
            if key not in KEYS:
                raise ValueError(f"conf file must contain the following fields: {KEYS}.")
        if not os.path.exists(conf[TMP_DIR]):
            print(f"tmp directory created: {TMP_DIR}.")
            os.mkdir(conf[TMP_DIR])

        tmp_masks = f"{conf[TMP_DIR]}/masks"
        if not os.path.exists(tmp_masks):
            print(f"tmp  sub-directory created: {tmp_masks}.")
            os.mkdir(tmp_masks)

        if not os.path.exists(conf[MASK_DIR]):
            print(f"tmp directory created: {MASK_DIR}.")
            os.mkdir(conf[MASK_DIR])

        if not os.path.exists(conf[SVS_DIR]):
            raise FileNotFoundError(f"svs directory {conf[SVS_DIR]} does not exist. Processing not possible.")

        if not os.path.isfile(conf[MANIFEST_IN]):
            raise FileNotFoundError(f"manifest_in {conf[MANIFEST_IN]} not found.")

        if not os.path.isfile(conf[MANIFEST_OUT]):
            print(f"creating {conf[MANIFEST_OUT]}.")
            with open(conf[MANIFEST_OUT], 'w') as man:
                man.write(MANIFEST_HEADERS)        
        try:
            f = open(conf[UPLOAD_LOG], 'w')
            f.close()
        except:
            raise FileNotFoundError(f"upload_log cant be opened. {conf[UPLOAD_LOG]}.")

            
            
def check_manifest(manifest_file):
    lines = []
    with open(manifest_file, "r") as man:
        lines = man.readlines()
    if len(lines) == 0:
        raise MANIFEST_FORMAT_EXCEPTION("emtpy file.")
    if lines[0].strip() != MANIFEST_HEADERS.strip():
        raise MANIFEST_FORMAT_EXCEPTION("first line of manifest should be: " + MANIFEST_HEADERS)
    lines = lines[1:]
    i = 1
    for line in lines:
        if len(line.split("\t")) != len(MANIFEST_HEADERS.split("\t")):
            raise MANIFEST_FORMAT_EXCEPTION(f"incorrect format on line {i}: {line}.")
        i += 1
    
class svs_management:
    conf = {}    
    def __init__(self, conf):
        self.conf = conf

    def get_id_list(file):
        id_list = []
        with open(file, 'r') as man_fd:
            man = man_fd.readlines()
            print(man)
            for line in man:
                line = line.split("\t")
                id_list.append(line[0].strip())

        print(id_list)
        return id_list

    def get_new_svs(self):
        in_id_ls = svs_management.get_id_list(self.conf[MANIFEST_IN])
        out_id_ls = svs_management.get_id_list(self.conf[MANIFEST_OUT])
        new_svs = None
        for id in in_id_ls:
            if id not in out_id_ls:
                new_svs = id
                break
        return new_svs

    def find_id_from_file(self, svs_file):
        man_fd = open(self.conf[MANIFEST_IN], "r")
        for line in man_fd:
            if svs_file in line:
                return line.split("\t")[0]
        return None 

    def find_file_from_id(self, svs_id):
        man_fd = open(self.conf[MANIFEST_IN], "r")
        for line in man_fd:
            if svs_id in line:
                return line.split("\t")[1]
        return None

    def is_downloaded(self, svs_id):
        dir_ls = os.listdir(self.conf[SVS_DIR])
        svs_file = self.find_file_from_id(svs_id)
        print(dir_ls, svs_file)
        return svs_file in dir_ls
        

    def append_manifest_out(self, id, file_name, mask_file_name):
        with open(self.conf[MANIFEST_OUT], "a") as man_out:
            man_out.write(f"{id}\t{file_name}\t{mask_file_name}\n")

    def delete_svs(self, id):
        f_name = self.find_file_from_id(id)
        os.remove(f"{self.conf[SVS_DIR]}/{f_name}")
    
    def upload_log(self, id, err_code):
        with open(self.conf[UPLOAD_LOG], "a") as log_f:
            log_f.write(f"{id}, {err_code}\n")
            




