from Database.MongoDB.base import *


def create_user(user):
    return user_collection.insert_one(user)


def delete_user(user):
    return user_collection.delete_one(user)


def get_user(username):
    return user_collection.find_one({"username": username})
