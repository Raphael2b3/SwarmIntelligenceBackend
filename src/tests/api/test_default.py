from starlette.testclient import TestClient

from main import app

client = TestClient(app=app)


async def test_login_for_access_token():
    pass


async def test_get_context():
    pass


async def test_star():
    pass


async def test_report():
    pass


async def test_update_truth():
    client.post()



async def test_root():
    pass
