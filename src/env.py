import sys

from dotenv import dotenv_values

HOST: str = "0.0.0.0"
PORT: int = 5555

DB_CONNECTION_STRING: str = ""
DB_USERNAME: str = ""
DB_PASSWORD: str = ""
DB_DATABASE: str = "neo4j"
__SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200


def init(path_to_env="./.env"):
    global HOST, PORT, DB_DATABASE, DB_PASSWORD, DB_CONNECTION_STRING, DB_USERNAME, ALGORITHM, \
        ACCESS_TOKEN_EXPIRE_MINUTES, __SECRET_KEY

    config = dotenv_values(path_to_env)
    HOST = config["HOST"]
    PORT = int(config["PORT"])

    DB_CONNECTION_STRING = config["DB_CONNECTION_STRING"]
    DB_USERNAME = config["DB_USERNAME"]
    DB_PASSWORD = config["DB_PASSWORD"]
    DB_DATABASE = config["DB_DATABASE"]
    __SECRET_KEY = config["__SECRET_KEY"]
    ALGORITHM = config["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])
