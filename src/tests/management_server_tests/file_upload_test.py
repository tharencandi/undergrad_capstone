import pytest
import os
import io
import shutil
from management_app.app import app
from management_app.fs import DATA_DIR

TMP_DIR="temp_mgmt_server"
RESOURCES="src/tests/resources"
@pytest.fixture()
def test_client():
    os.mkdir(TMP_DIR)
    app.config[DATA_DIR] = TMP_DIR
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    shutil.rmtree(TMP_DIR)
    # os.remove(TMP_DIR)
    ctx.pop()


def test_basic_upload(test_client):
        indata = io.BytesIO(b"data")
        data = dict(file=indata, filename="file")
        res = test_client.post("/GBM/uuid/mask", content_type='multipart/form-data')
        assert res.status_code == 200
        assert os.path.exists("temp_mgmt_server/uuid.mask")
        with open(TMP_DIR + "/uuid", "rb") as o:
            assert o.read() == indata


def test_basic_upload2(test_client):
    with open(RESOURCES + "/2.mask", "rb") as f:
        indata = f.read()
        data = dict(file=indata, filename="1.mask")
        res = test_client.post("/GBM/uuid/mask")
        assert res.status_code == 200
        assert os.path.exists("temp_mgmt_server/1.mask")
        with open(TMP_DIR + "/2.mask", "rb") as o:
            assert o.read() == indata

def test_reupload(test_client):
    indata = indata = io.BytesIO(b"data")
    data = dict(file=indata, filename="1.mask")
    res = test_client.post("/GBM/uuid/mask")
    assert res.status_code == 200
    assert os.path.exists("temp_mgmt_server/1.mask")
    with open(TMP_DIR + "/1.mask", "rb") as o:
        assert o.read() == indata

    with open(RESOURCES + "2.mask", "rb") as f:
        second_data = f.read()
        data = dict(file=indata, filename="2.mask")
        res = test_client.post("/GBM/uuid/mask")
        assert res.status_code == 409
        assert os.path.exists("temp_mgmt_server/1.mask")
        with open(TMP_DIR + "/1.mask", "rb") as o:
            assert o.read() == indata




