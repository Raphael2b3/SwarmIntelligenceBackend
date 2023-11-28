import dotenv

import controller
import security
from api.tests.setup.fill_sample_db import run


def test():

    dotenv.load_dotenv("api/tests/setup/.env")
    controller.init()
    security.init()

    run()

