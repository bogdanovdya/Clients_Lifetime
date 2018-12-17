import pandas as pd
from datetime import datetime, timedelta
from IApplication import *


class IndexApplication(IApplication):

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
                    IndexApplication.save_auth(cls)
                    return ret_arr

            return make_pagination

    def send_message(self, title, content):
        """
        Отправляет сообщение в живую ленту Битрикс24
        :param title: string
        :param content: string
        :return:
        """
        self.bx24.call('log.blogpost.add', {"POST_TITLE": title, "POST_MESSAGE": content})

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

    def get_cmp_ids(self, start=0, arr=[], days_start=365, days_finish=0):
        """
        Возвращает список ID компаний, которые имели коммерческую выгода за последний год
        :param start: pagination counter
        :param arr: result list
        :param days_start: begin of time_period
        :param days_finish: end of time_period
        :return: list
        """
        if start == 0:
            cmp_ids = []
        else:
            cmp_ids = arr

        finish_date = datetime.today() - timedelta(days=days_finish)
        start_date = datetime.today() - timedelta(days=days_start)
        inv_list = self.bx24.call('crm.invoice.list', {'ORDER': {'UF_COMPANY_ID': 'asc'}},
                                  {'FILTER': {'<DATE_BILL': finish_date,
                                              '>UF_COMPANY_ID': 1}},
                                  {'SELECT': ['UF_COMPANY_ID']}, {'start': start})
        if 'result' in inv_list:
            cmp_ids.extend(inv_list['result'])
        if 'next' in inv_list:
            return self.get_cmp_ids(start=start + 50, arr=cmp_ids, days_start=days_start, days_finish=days_finish)
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

        return {'cmp_list': cmp_list, 'deal_list': deal_list, 'inv_list': invoice_list, 'quote_list': quote_list}


