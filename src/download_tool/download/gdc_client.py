import requests
import shutil
import json
import logging
import functools
import gzip
from requests import HTTPError
from integrity import *

TEMP_FILE_POSTFIX = ".tmp"

class gdc_client:
    def __init__(self):
        self.data_url = "https://api.gdc.cancer.gov/data"

    def download_file(self, uuid: str, md5sum: str, filename: str):
        param = json.dumps({"ids": uuid})

        logging.info("Beginning download for uuid: %s, filename %s", uuid, filename)
        res = requests.post(
            self.data_url, data=param, headers={"Content-Type": "application/json"}
        )
        try:
            res.raise_for_status()
            is_valid_res = byte_obj_checksum(res.content, md5sum)
            if not is_valid_res:
                raise DownloadError(reason="Response content did not match checksum.")
            with open(filename, "wb") as f:
                f.write(res.content)

            verified_write = file_checksum(filename, md5sum)
            if not verified_write:
                raise DownloadError(
                    reason="Data written to file did not match checksum"
                )
            logging.info("Download finished for uuid %s, filename %s", uuid, filename)
        except HTTPError:
            logging.exception("HTTP request failed")
            raise DownloadError(reason="HTTPError")
        except IOError:
            logging.exception("Unable to write response content to file.")
            raise DownloadError(reason="Unable to write response content to file.")

    def mk_tmp_unzip(zipped_path):
        with gzip.open(zipped_path, "rb") as f_in:
            with open(zipped_path + TEMP_FILE_POSTFIX, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return zipped_path + TEMP_FILE_POSTFIX
        

    def stream_download_file(self, uuid: str, md5sum: str,  out_path: str,  decode_content=False):
        param = json.dumps({"ids": uuid})
        headers={
            "Content-Type": "application/json",
            "Accept-Encoding":  "gzip"
        }
        logging.info("Beginning download for uuid: %s, filename %s", uuid, out_path)
        try:
            with requests.post(
                self.data_url, data=param, headers=headers, stream=True
            ) as r:
                print(r.headers)
                input()
                r.raise_for_status()
                if decode_content:
                    response.raw.read = functools.partial(response.raw.read, decode_content=True)
                with open(out_path, "wb") as out:
                    shutil.copyfileobj(r.raw, out)
                
                is_valid = False
                if  not decode_content:
                    temp_f = self.gunzip(out_path)
                    is_valid = file_checksum(temp_f, md5sum)
                    os.remove(temp_f)
                else:
                    is_valid = file_checksum(fname, md5sum)
                
                if not is_valid:
                    raise DownloadError(
                        reason="Data written to file did not match checksum"
                    )
                logging.info("Download finished for uuid %s, filename %s", uuid, filename)
        except HTTPError:
            logging.exception("HTTP request failed")
            raise DownloadError(reason="HTTPError")
        except IOError:
            logging.exception("Unable to write response content to file.")
            raise DownloadError(reason="Unable to write response content to file.")
                

            
         




