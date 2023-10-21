from starlette.testclient import TestClient

from main import app

client = TestClient(app=app)


async def test_create():
    pass


async def test_delete():
    pass


async def test_change_password():
    pass
