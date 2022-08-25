import requests, json, logging
from requests import HTTPError
from integrity import *


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
