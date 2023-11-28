import api
import env
import host_infos
import db


def setup():
    env.init(".env")  # load env vars

    host_infos.print_host_name()  # show host name

    db.init(uri=env.DB_CONNECTION_STRING, database=env.DB_DATABASE, auth=(env.DB_USERNAME, env.DB_PASSWORD))  # init db


def teardown():
    db.close()


def start():
    api.run(host=env.HOST, port=env.PORT)  #


def test():
    pass  # Test enviroment and connections


if __name__ == '__main__':
    setup()
    test()
    start()
    teardown()
