import unittest
from app import app, db
from models import PortalAuth


class ConnectTest(unittest.TestCase):

    def test_db_conn(self):
        auth_info = PortalAuth(portal='portal', access_token='access_token', refresh_token='refresh_token')
        db.session.add(auth_info)
        db.session.commit()
        auth_info = PortalAuth.query.filter_by(portal='portal').first()
        access_token = auth_info.access_token
        self.assertEqual(access_token, 'access_token')


class AppTest(unittest.TestCase):
    """"""""


if __name__ == '__main__':
    unittest.main()
