from pydantic import BaseModel

import models.project
from const import DB_COLLECTION_NAME_PROJECTS

from services.dbcontroller import projectsDB


def create(doc: models.project.Project):
    return projectsDB.insert_one(doc.model_dump())


def delete(doc: models.project.Project):
    return projectsDB.delete_one(doc.model_dump())


class ProjectQuery(BaseModel):
    filter: models.project.Project
    limit: int = 8
    skip: int = 0
    depth: int = 1
    sort_method: str = None


def get_many(doc: ProjectQuery):
    return projectsDB.find(*doc.model_dump())


def get_one(doc:models.project.Project):
    return projectsDB.find_one(doc.model_dump())
