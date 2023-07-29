from controller import *
from models.user import User, UserDB
from models.statement import Statement, StatementDB

if __name__ == '__main__':
    users.create(UserDB(username="kokus", hashed_password="dfhdfkjghkjfdgkldf"))

    statements.create(StatementDB(value="Wahrheiten sdsada Wahr"))
    user = users.get({"username": "kokus"})
    print(user)
