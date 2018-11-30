from bitrix24.bitrix24 import Bitrix24
from tools.db_connect import *


class Application:
    """
    TODO переделать get_data под батч и добавить догрузку
    """
    instance = None

    def __new__(cls, domain, lang, auth_token, refresh_token):
        if cls.instance is None:
            cls.instance = super(Application, cls).__new__(cls)
        return cls.instance

    def __init__(self, domain, lang, auth_token, refresh_token):
        self.domain = domain.split('.bitrix24')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = refresh_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)

    def save_auth(self):
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    def get_cmp_list(self):
        cmp_list = self.bx24.call('crm.company.list')
        return cmp_list

    def get_data(self, cmp_ids):
        cmp_list = self.bx24.call('crm.company.list', {'ORDER': {'ID': 'asc'}}, {'FILTER': {'ID': cmp_ids}})
        deal_list = self.bx24.call('crm.deal.list', {'ORDER': {'COMPANY_ID': 'asc'}},
                                   {'FILTER': {'COMPANY_ID': cmp_ids}})
        invoice_list = self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                                      {'FILTER': {'UF_COMPANY_ID': cmp_ids}})

        return [cmp_list, deal_list, invoice_list]
