import projectController, statementController, userController
from Database.Models.user import User
from Database.Models.statement import Statement

if __name__ == '__main__':
    userController.create_user(User(username="kokus", hashed_password="dfhdfkjghkjfdgkldf").model_dump())

    statementController.create_statement(Statement(value="Wahrheiten sdsada Wahr").model_dump())
    user = userController.get_user({"username": "kokus"})
    print(user)
