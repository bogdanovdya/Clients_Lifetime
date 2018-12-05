import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
from bitrix24.bitrix24 import Bitrix24
from tools.db_connect import *


class Application:
    """
    TODO разобраться с возвратом прошлого вызова get_companies()
    """
    def __init__(self, domain, lang, auth_token, ref_token):
        self.domain = domain.split('.bitrix24')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = ref_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)

    class Decorators:
        @classmethod
        def list_decorator(cls, foo):
            def make_pagination(cls, cmp_ids, start=0, arr=[]):
                ids = cmp_ids
                ret_arr = arr
                listing = foo(cls, ids, page=start)
                if 'result' in listing:
                    ret_arr.extend(listing['result'])
                if 'next' in listing:
                    return make_pagination(cls, ids, start=start + 50, arr=ret_arr)
                else:
                    return ret_arr

            return make_pagination

    def save_auth(self):
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    @Decorators.list_decorator
    def get_companies(self, cmp_ids, page=0):
        return self.bx24.call('crm.company.list', {'ORDER': {'ID': 'asc'}}, {'FILTER': {'ID': cmp_ids}},
                              {'SELECT': ['TITLE', 'COMPANY_TYPE', 'INDUSTRY', 'REVENUE', 'EMPLOYEES']},
                              {'start': page})

    @Decorators.list_decorator
    def get_deals(self, cmp_ids, page=0):
        return self.bx24.call('crm.deal.list', {'ORDER': {'COMPANY_ID': 'asc'}}, {'FILTER': {'COMPANY_ID': cmp_ids}},
                              {'SELECT': ['PROBABILITY', 'OPPORTUNITY', 'BEGINDATE', 'CLOSEDATE', 'CLOSED',
                                          'COMPANY_ID']}, {'start': page})

    @Decorators.list_decorator
    def get_invoices(self, cmp_ids, page=0):
        return self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                              {'FILTER': {'UF_COMPANY_ID': cmp_ids}},
                              {'SELECT': ['DATE_BILL', 'DATE_PAYED', 'DATE_PAY_BEFORE', 'PRICE', 'PAYED',
                                          'STATUS_ID', 'UF_COMPANY_ID']}, {'start': page})

    @Decorators.list_decorator
    def get_quotes(self, cmp_ids, page=0):
        return self.bx24.call('crm.quote.list', {'ORDER': {'COMPANY_ID': 'asc'}}, {'FILTER': {'COMPANY_ID': cmp_ids}},
                              {'SELECT': ['COMPANY_ID', 'CLOSED', 'CLOSEDATE', 'DATE_CREATE', 'DEAL_ID',
                                          'OPPORTUNITY', 'STATUS_ID']}, {'start': page})

    def get_cmp_ids(self, start=0, arr=[]):
        start = start
        ret_arr = arr
        date = datetime.today() - timedelta(days=365 * 3)
        inv_list = self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                                  {'FILTER': {'>DATE_BILL': date, '>UF_COMPANY_ID': 1}},
                                  {'SELECT': ['UF_COMPANY_ID']}, {'start': start})
        if 'result' in inv_list:
            ret_arr.extend(inv_list['result'])
        if 'next' in inv_list:
            return self.get_cmp_ids(start=start + 50, arr=ret_arr)
        else:
            cmp_ids = pd.DataFrame(ret_arr)
            cmp_ids = cmp_ids.drop_duplicates('UF_COMPANY_ID')
            ret_arr = cmp_ids['UF_COMPANY_ID'].tolist()
            return ret_arr

    def get_data(self, cmp_ids):
        """
        по массиву айдишников компаний возвращает всякую дичь по ним
        :param cmp_ids: list
        :return: list
        """
        cmp_list = self.get_companies(cmp_ids)
        deal_list = self.get_deals(cmp_ids)
        invoice_list = self.get_invoices(cmp_ids)
        quote_list = self.get_quotes(cmp_ids)

        cmp_df = pd.DataFrame(cmp_list)
        # cmp_df.to_csv('cmp.csv', sep=";", index=False)
        deal_df = pd.DataFrame(deal_list)
        # deal_df.to_csv('deal.csv', sep=";", index=False)
        inv_df = pd.DataFrame(invoice_list)
        # inv_df.to_csv('inv.csv', sep=";", index=False)
        quote_df = pd.DataFrame(quote_list)
        # quote_df.to_csv('quote.csv', sep=";", index=False)
        # ret_df = cmp_df.merge(deal_df, left_on='ID', right_on='COMPANY_ID', how='outer')
        # ret_df = ret_df.merge(inv_df, left_on='COMPANY_ID', right_on='UF_COMPANY_ID', how='outer')
        print('------------------------------------------------------------------------------------------------')
        print(cmp_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(deal_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(inv_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(quote_df.head())
        # qwer = ret_df.as_matrix()
        return [cmp_list, deal_list, invoice_list, quote_list]
