import pytest
from os.path import join, expanduser
from webportal.webportal import application
import io


def test_delete():
    client = application.test_client()

    home = expanduser("~")
    WEB_PORTAL_DIR=join(home, ".glioblastoma_portal", "")
    DATA_DIR = join(WEB_PORTAL_DIR, "scans/")

    data = {"dir": DATA_DIR}
    response = client.post('/dir', query_string = data)

    with open('./scans/111/111.svs', 'rb') as scan:
        imgStringIO1 = io.BytesIO(scan.read())
        
    image_name = "test.svs"
    data = { 'file': (imgStringIO1,image_name) }
    response = client.post("/scan", data = data)
    
    uuid = response.data.decode('utf-8')
    uuid = uuid.strip('\n')
    uuid = uuid.strip('"')
    data = {"ids[]": uuid, "extension[]":"svs"}
    response2 = client.delete('/scan', query_string = data)

    assert response2.data.decode('utf-8') == '"DONE"\n'
