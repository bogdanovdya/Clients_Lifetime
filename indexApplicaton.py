from bitrix24.bitrix24 import Bitrix24
from tools.db_connect import *
import numpy as np
import pandas as pd


class Application:
    """
    TODO переделать get_data под батч и добавить догрузку
    """
    instance = None

    def __new__(cls, domain, lang, auth_token, ref_token):
        if cls.instance is None:
            cls.instance = super(Application, cls).__new__(cls)
        return cls.instance

    def __init__(self, domain, lang, auth_token, ref_token):
        self.domain = domain.split('.bitrix24')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = ref_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)

    def save_auth(self):
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    def get_cmp_list(self):
        cmp_list = self.bx24.call('crm.company.list', {'ORDER': {'ID': 'asc'}}, {'SELECT': ['TITLE']})
        return cmp_list

    def get_data(self, cmp_ids):
        """
        по массиву айдишников компаний возвращает всякую дичь по ним
        :param cmp_ids: list
        :return: list
        """
        cmp_list = self.bx24.call('crm.company.list', {'ORDER': {'ID': 'asc'}}, {'FILTER': {'ID': cmp_ids}},
                                  {'SELECT': ['TITLE', 'COMPANY_TYPE', 'INDUSTRY', 'REVENUE', 'EMPLOYEES']})

        deal_list = self.bx24.call('crm.deal.list', {'ORDER': {'COMPANY_ID': 'asc'}},
                                   {'FILTER': {'COMPANY_ID': cmp_ids}},
                                   {'SELECT': ['PROBABILITY', 'OPPORTUNITY', 'BEGINDATE', 'CLOSEDATE', 'CLOSED',
                                               'COMPANY_ID']})

        invoice_list = self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                                      {'FILTER': {'UF_COMPANY_ID': cmp_ids}},
                                      {'SELECT': ['DATE_BILL', 'DATE_PAYED', 'DATE_PAY_BEFORE', 'PRICE', 'PAYED',
                                                  'STATUS_ID', 'UF_COMPANY_ID']})

        quote_list = self.bx24.call('crm.quote.list', {'ORDER': {'COMPANY_ID': 'asc'}},
                                    {'FILTER': {'COMPANY_ID': cmp_ids}},
                                    {'SELECT': ['COMPANY_ID', 'CLOSED', 'CLOSEDATE', 'DATE_CREATE', 'DEAL_ID',
                                                'OPPORTUNITY', 'STATUS_ID']})

        cmp_df = pd.DataFrame(cmp_list['result'])
        deal_df = pd.DataFrame(deal_list['result'])
        inv_df = pd.DataFrame(invoice_list['result'])
        quote_df = pd.DataFrame(quote_list['result'])
        #ret_df = cmp_df.merge(deal_df, left_on='ID', right_on='COMPANY_ID', how='outer')
        #ret_df = ret_df.merge(inv_df, left_on='COMPANY_ID', right_on='UF_COMPANY_ID', how='outer')
        print(cmp_list)
        print('------------------------------------------------------------------------------------------------')
        print(cmp_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(deal_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(inv_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(quote_df.head())
        #qwer = ret_df.as_matrix()
        return [cmp_list['result'], deal_list['result'], invoice_list['result'], quote_list['result']]
