import unittest
from bx24_tools.bx24_connect import B24Connect
from bx24_tools.db_connect import DBConnect


class ConnectTest(unittest.TestCase):

    def test_bx24_conn(self):
        auth = B24Connect.auth('das', 'asd')
        self.assertEqual(auth['err'], False)


if __name__ == '__main__':
    unittest.main()
