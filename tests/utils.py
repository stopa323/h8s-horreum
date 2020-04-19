import unittest

from mongoengine import connect, disconnect


class DBMock(unittest.TestCase):

    def setUp(self):
        # super(DBMock, self).setUp()
        connect('mongoenginetest', host='mongomock://localhost')

    def tearDown(self):
        disconnect()
