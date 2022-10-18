import logging
from Crypto.Hash import MD5

CHUNK_SIZE = 1024

logger = logging.getLogger("download_tool")
def file_checksum(fname, md5sum):
    h = MD5.new()
    try:
        with open(fname, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest() == md5sum
    except (TypeError, ValueError):
        logger.exception("Unable to hash file.")
    except IOError:
        logger.exception("Unable to hash file.")

    return False


def byte_obj_checksum(obj, md5sum):
    try:
        h = MD5.new()
        h.update(obj)
        return h.hexdigest() == md5sum
    except (TypeError, ValueError):
        logger.exception("Unable to hash object.")
        return False
