import pytest
import unittest.mock as um
from download_tool.download.gdc_client import *

# def mocked_requests_post_valid(*args, **kwargs):
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code
#             self.content = ""

#         def json(self):
#             return self.json_data

#     return MockResponse(None, 404)

def test_gdc_client():
    assert gdc_client() != None
    assert isinstance(gdc_client(), gdc_client) == True

# def test_gdc_client_download_file():
#     gdc = gdc_client()
