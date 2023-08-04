from pydantic import BaseModel

import models.project
from models.user import User
from services.dbcontroller import projectsDB


def create(doc: models.project.Project):
    return projectsDB.insert_one(doc.model_dump())


def delete(doc: models.project.Project):
    return projectsDB.delete_one(doc.model_dump())


def get_many(doc: models.project.ProjectQuery, user: User):
    # exlcude author if author is not user
    return projectsDB.find(**doc.model_dump())


def get_one(doc: models.project.Project):
    return projectsDB.find_one(doc.model_dump())
