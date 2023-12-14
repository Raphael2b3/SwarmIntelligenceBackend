import host_infos
import api
import db

"""
api and db are implicitly loading env vars from .env file.
"""
if __name__ == '__main__':
    host_infos.print_host_name()  # show host name

    api.run()

    db.close()
