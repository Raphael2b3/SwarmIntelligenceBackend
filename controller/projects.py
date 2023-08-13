from pydantic import BaseModel

import models.project
from models.user import User

def create(doc: models.project.Project):
    return


def delete(doc: models.project.Project):
    return

def get_many(doc: models.project.ProjectQuery, user: User):
    # exlcude author if author is not user
    return

def get_one(doc: models.project.Project):
    return