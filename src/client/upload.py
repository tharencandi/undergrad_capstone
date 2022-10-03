import os
import requests

NGROK_ENDPOINT="https://jtjkrajnvdexwo.glioblastoma.au.ngrok.io"

GBM="GBM"
LGG="LGG"

MASK="mask"

MASK_ALREADY_UPLOADED=409
MASK_UPLOAD_SUCCESS=200
MASK_UPLOAD_FAILED=500
CLIENT_ERROR=404


class MaskUploader:

    def __init__(self, username, password):
        self.session = requests.Session()
        self.session.auth = (username, password)
     

    def upload_mask(self, case, uuid, local_fpath):
        """Uploads a mask to the server.

        Args:
            case: either GBM or LGG
            uuid: The uuid of the svs from which the mask was generated
            local_fpath: The filepath as a string to the local copy of the mask
                                     which should be sent

        Returns: An integer representing the status of the upload. See constants above.

        Raises:
        - In the event of a connection error,   requests.exceptions.ConnectionError() will be raised
        - In the event of a timeout error, requests.exceptions.Timeout() will be raised.
        """
        if not (case == GBM or case == LGG):
            raise ValueError("Invalid case.")

        url = NGROK_ENDPOINT + "/" + case + "/" + uuid + "/" + MASK

        r = self.session.post(url, files={"file": open(local_fpath, "r")})

        if r.status_code == 200:
            return MASK_UPLOAD_SUCCESS
        elif r.status_code == 409:
            return MASK_ALREADY_UPLOADED
        elif r.status_code == 404:
            return CLIENT_ERROR
        else:
            return MASK_UPLOAD_FAILED

