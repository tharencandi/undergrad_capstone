import pytest
import unittest.mock as um
from Crypto.Hash import MD5
from download_tool.integrity import *

def test_byte_object_checksum():

    # negative tests where types are wrong
    # no exception should be raised but it should
    # return false 
    assert byte_obj_checksum(None, "anything") == False
    assert byte_obj_checksum("string", "anything") == False
    assert byte_obj_checksum(1, "anything") == False

    # correct hash
    bo = bytes("a string", 'utf-8')
    h = MD5.new()
    h.update(bo)
    hd = h.hexdigest()
    assert byte_obj_checksum(bo, hd) == True

    # incorrect hash
    assert byte_obj_checksum(bo, "anything") == False
    assert byte_obj_checksum(bo, "") == False

def test_file_checksum():
    # invalid filename types
    assert file_checksum(None, "anything") == False
    assert file_checksum(1, "anything") == False

    bo = bytes("a string", 'utf-8')
    h = MD5.new()
    h.update(bo)
    hd = h.hexdigest()
    with um.patch('builtins.open', um.mock_open(read_data=bo)):

        #  correct checksum
        assert file_checksum("a_file.svs", hd) == True
    
        # incorrect checksum
        assert file_checksum("a_file.svs", "incorrect") == False

    with um.patch('builtins.open', um.mock_open(read_data="")):
        # incorrect checksum
        assert file_checksum("a_file.svs", "") == False


