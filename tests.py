import unittest
from bx24_tools.bx24_connect import B24Connect
from bx24_tools.db_connect import DBConnect
from mysql.connector import MySQLConnection


class ConnectTest(unittest.TestCase):

    def test_bx24_conn(self):
        auth = B24Connect.auth('das', 'asd')
        self.assertEqual(auth['err'], False)

    def test_db_conn(self):
        conn = DBConnect.connect()
        isclass = isinstance(conn, MySQLConnection)
        self.assertEqual(isclass, True)
        conn.close()


class AppTest(unittest.TestCase):
    """"""""


if __name__ == '__main__':
    unittest.main()
