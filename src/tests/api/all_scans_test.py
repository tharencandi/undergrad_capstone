import pytest
from os.path import join, expanduser
from webportal.webportal import application


def test_all_scans():
    client = application.test_client()

    home = expanduser("~")
    WEB_PORTAL_DIR=join(home, ".glioblastoma_portal", "")
    DATA_DIR = join(WEB_PORTAL_DIR, "scans/")
    
    data = {"dir": DATA_DIR}
    response = client.post('/dir', query_string = data)

    assert response.status_code == 200

    response = client.get('/all')


    assert response.status_code == 200
    assert response.data.decode('utf-8') == '{}\n'
