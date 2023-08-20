from const import DB_CONNECTION_STRING
from neo4j import Driver, AsyncGraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = DB_CONNECTION_STRING

AUTH = ("neo4j", "00000000")

# TODO Create indeces
"""
INDECES: 
    Statement TEXT
    PROJECT TEXT
    Statement ID
    PROJECT ID
    CONNECTION ID?
    USERNAME 


"""
driver: Driver


def get_driver():
    return driver


def init():
    global driver
    driver = AsyncGraphDatabase.driver(uri=URI, auth=AUTH, database="neo4j")
