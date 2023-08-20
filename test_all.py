import unittest
from controller.connections import create_connection, weight_connection, delete_connection
from controller.statements import create
import controller.users as usercntrl
from services.dbcontroller import get_driver

# TODO Make good tests
class TestConnectionController(unittest.TestCase):
    startId = 0
    stopId = 1
    supports = True
    username = "Peter"

    def test_create_connection(self):
        create_connection(stopId=self.stopId, startId=self.startId, supports=self.supports,
                          username=self.username)  # add assertion here

    def test_weight_connection(self):
        weight_connection(stopId=self.stopId, startId=self.startId, weight=0.5,
                          username=self.username)  # add assertion here

    def test_delete_connection(self):
        delete_connection(stopId=self.stopId, startId=self.startId, username=self.username, )  # add assertion here

    def test_create_test_data(self):
        usercntrl.create(username="tim", hashed_password="2134321")


if __name__ == '__main__':
    unittest.main()
