from Database.MongoDB.base import *


def create_project(project):
    return project_collection.insert_one(project)


def delete_project(project):
    return project_collection.delete_one(project)


def get_project(project):
    return project_collection.find_one(project)
