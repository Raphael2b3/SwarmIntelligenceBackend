from dotenv import dotenv_values

config = dotenv_values("./.env")

HOST = config["HOST"]
PORT = int(config["PORT"])

DB_CONNECTION_STRING = config["DB_CONNECTION_STRING"]
DB_USERNAME = config["DB_USERNAME"]
DB_PASSWORD = config["DB_PASSWORD"]

__SECRET_KEY = config["__SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])
