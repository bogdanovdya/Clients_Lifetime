import unittest
from bx24_tools.bx24_connect import B24Connect


class ConnectTest(unittest.TestCase):

    def test_bx24_conn(self):
        auth = B24Connect.auth('das', 'asd')
        self.assertEqual(auth['err'], False)


if __name__ == '__main__':
    unittest.main()
