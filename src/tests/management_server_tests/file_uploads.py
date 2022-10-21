import pytest
import os
import shutil
from management_app.app import app, DATA_DIR

TMP_DIR="temp_mgmt_server"
@pytest.fixture()
def test_client():
    os.mkdir(TMP_DIR)
    app.config[DATA_DIR] = TMP_DIR
    testing_client = app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    shutil.rmtree(TMP_DIR)
    ctx.pop()


def test_basic_upload(test_client):



