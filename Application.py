import sys
from bitrix24.bitrix24 import Bitrix24
from bx24_tools.bx24_connect import *
from bx24_tools.db_connect import *


class Application:
    """
    TO DO проверка логина, отправка батча
    """
    def __init__(self):
        self.ar_access_params = ()
        self.b24_error = None
        self.is_background_mode = False
        self.ar_b24_apps = None
        self.is_token_refreshed = None
        self._db_collection = {}

    @staticmethod
    def save_auth(domain, token, refresh_token, member_id):
        DBConnect.save_auth(domain, token, refresh_token, member_id)

    @staticmethod
    def get_auth_from_db():
        auth = B24Connect.auth()
        if(auth['err'] is not True):
            raise SystemExit(1)


if __name__ == '__main__':
        app = Application
        app.get_auth_from_db()
