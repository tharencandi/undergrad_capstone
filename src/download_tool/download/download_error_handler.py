import logging

logger = logging.getLogger(("download_error"))

APPEND_FAIL_MSG = """
Unable to append component to download error message while handling a download error.
"""


def download_error_handler(fpath, *args):
    err_str = ""
    for arg in args:
        err_str = append_err_comp(err_str, arg)

    with open(fpath, "a") as f:
        f.write(err_str)


def append_err_comp(msg, comp):
    try:
        return msg + str(comp) + "\t"

    except (ValueError, TypeError):
        logger.exception(APPEND_FAIL_MSG)
