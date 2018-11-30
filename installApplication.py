import sys
from bitrix24.bitrix24 import Bitrix24
from tools.bx24_connect import *
from tools.db_connect import *


class InstallApplication:
    def __init__(self, domain, lang, auth_token, refresh_token):
        self.domain = domain.split('.bitrix24')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = refresh_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)

    def save_auth(self):
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    def send_message(self, title, content):
        return self.bx24.call('log.blogpost.add', {"POST_TITLE": title, "POST_MESSAGE": content})

