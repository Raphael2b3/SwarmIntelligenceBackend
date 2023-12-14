import db
from tests.fill_sample_db import run


def test():
    run()

    db.close()
