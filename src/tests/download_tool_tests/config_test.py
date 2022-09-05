import pytest

from download_tool.config import *

def  test_field_validator():
    # Empty configuration
    empty =  {}
    single = {"first": None}
    int_key = {1: None}
    multiple_types = {1: None, "asd": None}
    normal = {"1": None, "2": None, "3": None}

    # missing fields
    with pytest.raises(KeyError):
        field_validator(empty, "missing_field")
        field_validator(normal, "missing_field")
        field_validator(single, "first", "second")
        field_validator(empty, "")
        field_validator(multiple_types,  1, "1")
    
    # no missing fields so no exceptions should be raised
    field_validator(empty)
    field_validator(single, "first")
    field_validator(int_key, 1)
    field_validator(multiple_types, 1, "asd")
    field_validator(normal, "1", "2", "3")

    # extra fields are allowed so no exceptions should be raised
    field_validator(normal, "1", "2")
    field_validator(single)
    field_validator(int_key)