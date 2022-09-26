from yaml import safe_load
import pytest
import CNN.file_management as file_management
import os
def test_no_man_in():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/no_man_in.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    with pytest.raises(FileNotFoundError):
        file_management.conf_init(p_conf)

def test_bad_fields():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/bad_fields.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    with pytest.raises(ValueError):
        file_management.conf_init(p_conf)
def test_bad_svs_dir():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/no_svs_dir.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    with pytest.raises(FileNotFoundError):
        file_management.conf_init(p_conf)
def test_no_man_out():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/no_man_out.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    file_management.conf_init(p_conf)
    assert os.path.isfile("src/tests/CNN_tests/svs_manager_tests/data/temp_test_manifest.out")
    os.remove("src/tests/CNN_tests/svs_manager_tests/data/temp_test_manifest.out")

def test_no_mask_dir():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/no_mask.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    file_management.conf_init(p_conf)
    assert os.path.isdir("src/tests/CNN_tests/svs_manager_tests/data/test_masks")
    os.rmdir("src/tests/CNN_tests/svs_manager_tests/data/test_masks")
def no_tmp_dir():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/no_tmp_dir.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    file_management.conf_init(p_conf)
    assert os.path.isdir("src/tests/CNN_tests/svs_manager_tests/data/test_tmp")
    os.rmdir("src/tests/CNN_tests/svs_manager_tests/data/test_tmp")
def test_all_good():
    p_conf = {}
    with open("src/tests/CNN_tests/svs_manager_tests/data/good.yaml", "r") as conf:
        p_conf =  safe_load(conf)
    try:
        file_management.conf_init(p_conf)
    except Exception as e:
        assert False, str(e)
