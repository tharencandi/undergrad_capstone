import requests
import os
import json
import logging
import gzip
import sys
import signal
from tqdm import tqdm
from requests import HTTPError

cdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cdir))

from download_tool.download.DownloadError import DownloadIntegrityError, DownloadError
from download_tool.integrity import *

PARTIAL_FILE_POSTFIX = ".part"

logger = logging.getLogger("download_tool")

class gdc_client:
    def __init__(self):
        self.data_url = "https://api.gdc.cancer.gov/data"

    def download_file(self, uuid: str, md5sum: str, filename: str):
        param = json.dumps({"ids": uuid})

        logger.info("Beginning download for uuid: %s, filename %s", uuid, filename)
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
            logger.info("Download finished for uuid %s, filename %s", uuid, filename)
        except HTTPError:
            logger.exception("HTTP request failed")
            raise DownloadError(reason="HTTPError")
        except IOError:
            logger.exception("Unable to write response content to file.")
            raise DownloadError(reason="Unable to write response content to file.")
        

    def stream_download_file(self, uuid: str, md5sum: str,  out_path: str,  chunk_size: int):
        param = json.dumps({"ids": uuid})
        headers={
            "Content-Type": "application/json",
            "Accept-Encoding":  "gzip"
        }
        logger.warn("Beginning download for uuid: %s, filename %s", uuid, out_path)
        try:
            # send request to begin download
            with requests.post(self.data_url, data=param, headers=headers, stream=True) as r:
                r.raise_for_status()

                #  stream data to temp file with .part postfix
                with open(out_path + PARTIAL_FILE_POSTFIX, "wb") as out:
                    pbar = tqdm(total=int(r.headers["content-length"]), unit="iB", unit_scale=True)
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        pbar.update(len(chunk))
                        out.write(chunk)
                    pbar.close()
            if not file_checksum(out_path + PARTIAL_FILE_POSTFIX, md5sum):
                raise DownloadIntegrityError()

            # data has been validated and downloaded, remove .part postfix 
            os.rename(out_path + PARTIAL_FILE_POSTFIX, out_path)
            logger.warn("Download finished for uuid %s, filename %s", uuid, out_path)
        except HTTPError as e:
            status = e.response.status_code
            msg = f"HTTPError  with code {status}"
            logger.exception(msg)
            raise DownloadError(msg)
        except IOError:
            logger.exception("Unable to write response content to file.")
            raise DownloadError("Unable to write response content to file.")


            
         




