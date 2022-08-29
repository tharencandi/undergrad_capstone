import logging
from Crypto.Hash import MD5

CHUNK_SIZE = 1024


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
        logging.exception("Unable to hash file.")
    except IOError:
        logging.exception("Unable to hash file.")

    return False


def byte_obj_checksum(obj, md5sum):
    h = MD5.new()
    try:
        h.update(obj)
        return h.hexdigest() == md5sum
    except (TypeError, ValueError):
        logging.exception("Unable to hash object.")
        return False
