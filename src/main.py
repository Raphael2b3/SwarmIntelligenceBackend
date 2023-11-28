import dotenv
import host_infos
import controller
import api
import security.jwt_auth


def setup():

    host_infos.print_host_name()  # show host name
    dotenv.load_dotenv(override=True)
    controller.init()
    security.init()

def test():
    pass  # Test enviroment and connections


def start():
    api.run()


def teardown():
    controller.close()


if __name__ == '__main__':
    setup()
    test()
    start()
    teardown()
