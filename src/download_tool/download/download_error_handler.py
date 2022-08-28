import logging

APPEND_FAIL_MSG = """
Unable to append component to download error message while handling a download error.
"""


def download_error_handler(fpath, *args):
    err_str = ""
    for arg in args:
        append_err_comp(err_str, arg)

    with open(fpath, "a") as f:
        f.write(err_str)


def append_err_comp(msg, comp):
    try:
        msg += str(comp) + "\t"
    except (ValueError, TypeError):
        logging.exception(APPEND_FAIL_MSG)
