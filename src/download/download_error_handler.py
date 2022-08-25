import logging

ERR_LOG_FILE = "download_failures.log"
APPEND_FAIL_MSG = """
Unable to append component to download error message while handling a download error.
"""


def download_error_handler(*args):
    err_str = ""
    for arg in args:
        append_err_comp(err_str, arg)

    with open(ERR_LOG_FILE, "a") as f:
        f.write(err_str)


def append_err_comp(msg, comp):
    try:
        msg += str(comp) + "\t"
    except (ValueError, TypeError):
        logging.exception(APPEND_FAIL_MSG)
