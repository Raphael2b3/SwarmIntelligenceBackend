from dotenv import dotenv_values

config = dotenv_values(".env")

HOST = config["HOST"]
PORT = config["PORT"]

DB_CONNECTION_STRING = config["DB_CONNECTION_STRING"]

