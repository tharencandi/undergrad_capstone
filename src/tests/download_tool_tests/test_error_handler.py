import pytest
import unittest.mock as um
from download_tool.download.download_error_handler import *


def test_append_err_comp():
    msg = ""
    comp = "test string"
    assert append_err_comp(msg, comp) == "test string\t"

    msg = ""
    comp = 12345
    assert append_err_comp(msg, comp) == "12345\t"

    msg = "original\t"
    comp = "test string"

    assert append_err_comp(msg, comp) == "original\ttest string\t"

    # bad types, but no exception
    msg = None
    comp = "string"
    append_err_comp(msg, comp)

    msg = ""
    comp = object()
    append_err_comp(msg, comp)
    
def test_download_error_handler():
    mk = um.mock_open()
    f = "file"
    with um.patch('builtins.open', mk, create=True):
        download_error_handler("file", "arg1", "arg2")
        mk.assert_called_with("file", "a")
        mk.return_value.write.assert_called_once_with("arg1\targ2\t")


