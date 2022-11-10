from tests.conftest import client


def tearDown(self):
    self.app_process.terminate()
    self.app_process.join()

def test_should_status_code_ok(client):
    resp = client.get('/')
    assert resp.status_code == 200
