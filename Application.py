import sys
from bitrix24.bitrix24 import Bitrix24
from bx24_tools.bx24_connect import *
from bx24_tools.db_connect import *


class Application:
    """
    TODO проверка логина, отправка батча
    """
    def __init__(self, domain, lang, auth_token, refreah_token):
        self.domain = domain.split('.')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = refreah_token
        self.save_auth()

    def save_auth(self):
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    def get_auth_from_db(self, domain, token):
        auth = B24Connect.auth(domain, token)
        if auth['err'] is True:
            return auth['app']
