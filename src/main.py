import dotenv
import host_infos
import db
import api


def setup():
    dotenv.load_dotenv()
    host_infos.print_host_name()  # show host name


def test():
    pass  # Test enviroment and connections


def start():
    api.run()


def teardown():
    db.close()


if __name__ == '__main__':
    setup()
    test()
    start()
    teardown()
