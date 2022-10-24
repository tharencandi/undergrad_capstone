import pytest
from requests import Session
from unittest.mock import MagicMock, patch

from client.upload import MaskUploader

@patch(Session, 'post')
def test_200(ms):
    up = MaskUploader("x", "y")
    up.session = ms
    res = MagicMock()
    res.status_code = 200
    mr.return_value = MagicMock(res)
    assert up.upload_mask("GBM", "uuid", "local") == 200

@patch(Session, 'post')
def test_200(ms):
    up = MaskUploader("x", "y")
    up.session = ms
    res = MagicMock()
    res.status_code = 409
    mr.return_value = MagicMock(res)
    assert up.upload_mask("GBM", "uuid", "local") == 409

@patch(Session, 'post')
def test_200(ms):
    up = MaskUploader("x", "y")
    up.session = ms
    res = MagicMock()
    res.status_code = 400
    mr.return_value = MagicMock(res)
    assert up.upload_mask("GBM", "uuid", "local") == 400

@patch(Session, 'post')
def test_200(ms):
    up = MaskUploader("x", "y")
    up.session = ms
    res = MagicMock()
    res.status_code = 500
    mr.return_value = MagicMock(res)
    assert up.upload_mask("GBM", "uuid", "local") == 500


@patch(Session, 'post')
def test_200(ms):
    up = MaskUploader("x", "y")
    up.session = ms
    res = MagicMock()
    res.status_code = 300
    mr.return_value = MagicMock(res)
    assert up.upload_mask("GBM", "uuid", "local") == 500