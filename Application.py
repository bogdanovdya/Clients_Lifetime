import sys
from bitrix24.bitrix24 import Bitrix24
from bx24_tools.bx24_connect import *
from bx24_tools.db_connect import *


class Application:
    """
    TODO проверка логина, отправка батча
    """
    def __init__(self):
        self.auth_token = ''
        self.ar_access_params = ()
        self.b24_error = None
        self.is_background_mode = False
        self.ar_b24_apps = None
        self.is_token_refreshed = None
        self._db_collection = DBConnect.select_token_collection()

    def save_auth(self, domain, token, refresh_token):
        DBConnect.save_auth(domain, token, refresh_token)

    def get_auth_from_db(self, domain, token):
        auth = B24Connect.auth(domain, token)
        if auth['err'] is True:
            return auth['app']


if __name__ == '__main__':
    app = Application()
    bx24 = Bitrix24('team', 'dasdasasdas')
