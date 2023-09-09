import sys

from dotenv import dotenv_values

config = dotenv_values("./.env")
if config:
    HOST = config["HOST"]
    PORT = int(config["PORT"])

    DB_CONNECTION_STRING = config["DB_CONNECTION_STRING"]
    DB_USERNAME = config["DB_USERNAME"]
    DB_PASSWORD = config["DB_PASSWORD"]

    __SECRET_KEY = config["__SECRET_KEY"]
    ALGORITHM = config["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])
else:
    print("no .env file provided!")
    HOST = "0.0.0.0"
    PORT = 5555

    DB_CONNECTION_STRING = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""

    __SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 43200
