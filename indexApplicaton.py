import pandas as pd
from datetime import datetime, timedelta
from bitrix24.bitrix24 import Bitrix24
from tools.db_connect import *


class Application:
    """
    TODO return get_data как словарь
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
            """
            Возвращает список 'result' пагинированного вызова bitrix24
            :param foo: function
            :return: list
            """
            def make_pagination(cls, cmp_ids, start=0, arr=[]):
                if start == 0:
                    ret_arr = []
                else:
                    ret_arr = arr
                listing = foo(cls, cmp_ids, page=start)
                if 'result' in listing:
                    ret_arr.extend(listing['result'])
                if 'next' in listing:
                    return make_pagination(cls, cmp_ids, start=start + 50, arr=ret_arr)
                else:
                    return ret_arr

            return make_pagination

    def save_auth(self):
        """
        Сохраняет данные OAuth в БД
        :return:
        """
        DBConnect.save_auth(self.domain, self.auth_token, self.ref_token)

    @Decorators.list_decorator
    def get_companies(self, cmp_ids, page=0):
        """
        Возвращает список словарей о компаниях
        :param cmp_ids: list
        :param page: int
        :return: list of dict
        """
        return self.bx24.call('crm.company.list', {'ORDER': {'ID': 'asc'}}, {'FILTER': {'ID': cmp_ids}},
                              {'SELECT': ['TITLE', 'COMPANY_TYPE']},
                              {'start': page})

    @Decorators.list_decorator
    def get_deals(self, cmp_ids, page=0):
        """
        Возвращает список словарей о сделках копаний
        :param cmp_ids: list
        :param page: int
        :return: list of dict
        """
        return self.bx24.call('crm.deal.list', {'ORDER': {'COMPANY_ID': 'asc'}}, {'FILTER': {'COMPANY_ID': cmp_ids}},
                              {'SELECT': ['PROBABILITY', 'OPPORTUNITY', 'BEGINDATE', 'CLOSEDATE', 'CLOSED',
                                          'COMPANY_ID']}, {'start': page})

    @Decorators.list_decorator
    def get_invoices(self, cmp_ids, page=0):
        """
        Возвращает список словарей об оплтах компаний
        :param cmp_ids: list
        :param page: int
        :return: list of dict
        """
        return self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                              {'FILTER': {'UF_COMPANY_ID': cmp_ids}},
                              {'SELECT': ['DATE_BILL', 'DATE_PAYED', 'DATE_PAY_BEFORE', 'PRICE', 'PAYED',
                                          'STATUS_ID', 'UF_COMPANY_ID']}, {'start': page})

    @Decorators.list_decorator
    def get_quotes(self, cmp_ids, page=0):
        """
        Возвращает список словарей о коммерческих предложенях компаний
        :param cmp_ids: list
        :param page: int
        :return: list of dict
        """
        return self.bx24.call('crm.quote.list', {'ORDER': {'COMPANY_ID': 'asc'}}, {'FILTER': {'COMPANY_ID': cmp_ids}},
                              {'SELECT': ['COMPANY_ID', 'CLOSED', 'CLOSEDATE', 'DATE_CREATE', 'DEAL_ID',
                                          'OPPORTUNITY', 'STATUS_ID']}, {'start': page})

    def get_cmp_ids(self, start=0, arr=[]):
        """
        Возвращает список ID компаний, которые имели коммерческую выгода за последний год
        :param start: pagination counter
        :param arr: result list
        :return: list
        """
        if start == 0:
            cmp_ids = []
        else:
            cmp_ids = arr

        date = datetime.today() - timedelta(days=365)
        inv_list = self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                                  {'FILTER': {'>DATE_BILL': date, '>UF_COMPANY_ID': 1}},
                                  {'SELECT': ['UF_COMPANY_ID']}, {'start': start})
        if 'result' in inv_list:
            cmp_ids.extend(inv_list['result'])
        if 'next' in inv_list:
            return self.get_cmp_ids(start=start + 50, arr=cmp_ids)
        else:
            # Очистка дубликатов через пандас, потому как массив словарей
            cmp_ids = pd.DataFrame(cmp_ids)
            if 'UF_COMPANY_ID' in cmp_ids:
                cmp_ids = cmp_ids.drop_duplicates('UF_COMPANY_ID')
                ret_arr = cmp_ids['UF_COMPANY_ID'].tolist()
                return ret_arr
            else:
                return None

    def get_data(self, cmp_ids):
        """
        по массиву айдишников компаний возвращает всякую дичь по ним
        :param cmp_ids: list
        :return: list of list of dicts
        """
        cmp_list = self.get_companies(cmp_ids)
        deal_list = self.get_deals(cmp_ids)
        invoice_list = self.get_invoices(cmp_ids)
        quote_list = self.get_quotes(cmp_ids)

        return [cmp_list, deal_list, invoice_list, quote_list]

    def get_data_set(self, cmp_ids):
        """
        Тестовая функция, чтоб наверника все получить, но долгим образом.
        :param cmp_ids:
        :return:
        """
        cmp_list, deal_list, inv_list, quo_list = [], [], [], []

        for id in cmp_ids:

            cmp_info = self.get_companies(id)
            if cmp_info:
                cmp_list.extend(cmp_info)

            deal_info = self.get_deals(id)
            if deal_info:
                deal_list.extend(deal_info)

            inv_info = self.get_invoices(id)
            if inv_info:
                inv_list.extend(inv_info)

            quo_info = self.get_quotes(id)
            if quo_info:
                quo_list.extend(quo_info)

        cmp_df = pd.DataFrame(cmp_list)
        cmp_df.to_csv('cmp.csv', sep=";", index=False)
        deal_df = pd.DataFrame(deal_list)
        deal_df.to_csv('deal.csv', sep=";", index=False)
        inv_df = pd.DataFrame(inv_list)
        inv_df.to_csv('inv.csv', sep=";", index=False)
        quote_df = pd.DataFrame(quo_list)
        quote_df.to_csv('quote.csv', sep=";", index=False)
        print('------------------------------------------------------------------------------------------------')
        print(cmp_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(deal_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(inv_df.head())
        print('------------------------------------------------------------------------------------------------')
        print(quote_df.head())

        return [cmp_list, deal_list, inv_list, quo_list]
