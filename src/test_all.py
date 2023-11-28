from api.tests.setup.fill_sample_db import run


def test_init():
    run(path_to_env="api/tests/setup/.env")

