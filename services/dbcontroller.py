from const import DB_CONNECTION_STRING
from neo4j import GraphDatabase, Driver

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

# TODO better driver management

def init():
    global driver
    driver = GraphDatabase.driver(uri=URI, auth=AUTH, database="neo4j")


def teardown():
    global driver
    driver.close()
