import pytest
import io

from webportal.webportal import application


def test_upload():
    client = application.test_client()

    data = {"dir": "./scans/"}

    response = client.post('/dir', query_string = data)

    # response = self.client.get(url_for("api.my-service"), query_string = data)

    assert response.status_code == 200
    
    with open('./scans/111/111.svs', 'rb') as scan:
        imgStringIO1 = io.BytesIO(scan.read())
        
    image_name = "test.svs"
    data = { 'file': (imgStringIO1,image_name) }
    response = client.post("/scan", data = data)
    

    # assert response.status_code == 200
    assert response.data.decode('utf-8') != ''

