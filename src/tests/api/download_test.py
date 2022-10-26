import pytest
from os.path import join, expanduser
from os import mkdir
from webportal.webportal import application
import io


def test_download():
    client = application.test_client()

    home = expanduser("~")
    WEB_PORTAL_DIR=join(home, ".glioblastoma_portal", "")
    DATA_DIR = join(WEB_PORTAL_DIR, "scans/")

    data = {"dir": DATA_DIR}
    response = client.post('/dir', query_string = data)


    # test_dir = DATA_DIR + "test_uuid"
    # mkdir(test_dir)
    # new_svs = open(test_dir + "/test.svs", "w")
    # new_svs.close()



    with open('./scans/111/111.svs', 'rb') as scan:
        imgStringIO1 = io.BytesIO(scan.read())
    image_name = "test.svs"
    data = { 'file': (imgStringIO1,image_name) }
    response = client.post("/scan", data = data)

    uuid = response.data.decode('utf-8').strip('\n')
    uuid = uuid.strip('"')


    # scan_path = join('.', '..', 'tests', 'api', 'scans')
    # data = {"dir": "./scans/"}
   

    assert response.status_code == 200
    # assert response.data.decode('utf-8') == '"DONE"\n'

    download_data = {"ids[]": uuid, "extension[]":"svs"}

    response = client.get('/scan', query_string = download_data)
    assert response.headers['Content-Disposition'] == 'inline; filename=test.svs'

