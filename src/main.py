import dotenv
import db
import host_infos
import api
import security.jwt


def setup():
    host_infos.print_host_name()  # show host name
    dotenv.load_dotenv(override=True)
    db.init()
    security.init()


def start():
    api.run()


def teardown():
    db.close()


if __name__ == '__main__':
    setup()
    start()
    teardown()
