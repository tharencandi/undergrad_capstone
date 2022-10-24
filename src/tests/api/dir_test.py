import pytest

from webportal.webportal import application


def test_dir():
    client = application.test_client()

    data = {"dir": "./scans/"}

    response = client.post('/dir', query_string = data)

    # response = self.client.get(url_for("api.my-service"), query_string = data)

    assert response.status_code == 200
    assert response.data.decode('utf-8') == '"DONE"\n'

    response2 = client.get('/dir')

    assert response2.data.decode('utf-8') == '"./scans/"\n'
    # assert response.data.decode('utf-8') == '"home page\n"'
