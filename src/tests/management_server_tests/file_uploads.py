import pytest
from management_app.app import app, DATA_DIR

@pytest.fixture()
def test_client():
    app.config[DATA_DIR] = "temp"
    testing_client = app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


def @pytest.fixture()

