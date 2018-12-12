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

    def create_bot(self):
        return self.bx24.call('imbot.register',
                              {
                                  'CODE': 'newbot',
                                  'TYPE': 'H',
                                  'EVENT_HANDLER': 'https://5.206.88.44/bot',
                                  'PROPERTIES': {
                                      'NAME': 'NewBot',
                                      'LAST_NAME': '',
                                      'COLOR': 'blue',
                                      'WORK_POSITION': 'data scientist'
                                  }
                              })

