import dotenv

import db
import security
from api.tests.setup.fill_sample_db import run


def test():
    dotenv.load_dotenv("api/tests/setup/.env")
    db.init()
    security.init()

    run()

    db.close()
