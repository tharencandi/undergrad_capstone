import requests
import shutil
import json
import logging
import functools
import gzip
import sys
import signal
from tqdm import tqdm
from requests import HTTPError
from integrity import *

TEMP_FILE_POSTFIX = ".tmp"

# def sig_handler(sig, frame):

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
        

    def stream_download_file(self, uuid: str, md5sum: str,  out_path: str,  chunk_size: int):
        param = json.dumps({"ids": uuid})
        headers={
            "Content-Type": "application/json",
            "Accept-Encoding":  "gzip"
        }
        logging.info("Beginning download for uuid: %s, filename %s", uuid, out_path)
        try:
            with requests.post(self.data_url, data=param, headers=headers, stream=True) as r:
                r.raise_for_status()
                with open(out_path, "wb") as out:
                    pbar = tqdm(total=int(r.headers["content-length"]), unit="iB", unit_scale=True)
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        pbar.update(len(chunk))
                        out.write(chunk)
                    pbar.close()
            if not file_checksum(out_path, md5sum):
                raise DownloadIntegrityError()

            logging.info("Download finished for uuid %s, filename %s", uuid, filename)
        except HTTPError as e:
            status = e.response.status_code
            msg = f"HTTPError  with code {status}"
            logging.exception(msg)
            raise DownloadError(msg)
        except IOError:
            logging.exception("Unable to write response content to file.")
            raise DownloadError("Unable to write response content to file.")


            
         




