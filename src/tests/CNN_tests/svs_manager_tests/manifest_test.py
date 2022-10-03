import CNN.file_management as file_management
import pytest 
REL_PATH = "src/tests/CNN_tests/svs_manager_tests/data/"
def test_empty_manifest():   
    with pytest.raises(file_management.MANIFEST_FORMAT_EXCEPTION):
        file_management.check_manifest(REL_PATH + "manifest_empty.txt")
    
def test_bad_tabbing():
    with pytest.raises(file_management.MANIFEST_FORMAT_EXCEPTION):
        file_management.check_manifest(REL_PATH + "manifest_bad_tab.txt")
def test_incorrect_fields():
    with pytest.raises(file_management.MANIFEST_FORMAT_EXCEPTION):
        file_management.check_manifest(REL_PATH + "manifest_bad_fields.txt")
def bad_entry():
    with pytest.raises(file_management.MANIFEST_FORMAT_EXCEPTION):
        file_management.check_manifest(REL_PATH + "manifest_bad_entry.txt")
