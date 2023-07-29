from Database.MongoDB.base import *


def create_statement(statement):
    return statement_collection.insert_one(statement)


def delete_statement(statement):
    return statement_collection.delete_one(statement)


def get_statement(statement):
    return statement_collection.find_one(statement)
