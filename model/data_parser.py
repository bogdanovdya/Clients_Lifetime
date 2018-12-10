import pandas as pd
import numpy as np


class DataParser:

    @staticmethod
    def _parse_companies(cmp_list):
        """
        Создает DataFrame компаний по списку словарей из запроса
        :param cmp_list: list of dicts
        :return: pandas.DataFrame
        """
        ret_df = pd.DataFrame(columns=['ID', 'TITLE', 'CMP_TYPE_CUSTOMER', 'CMP_TYPE_PARTNER'])

        if cmp_list:
            cmp_df = pd.DataFrame(cmp_list)

            cmp_df['CMP_TYPE_CUSTOMER'] = cmp_df['COMPANY_TYPE'].apply(lambda x: 1 if (x == 'CUSTOMER') else 0)
            cmp_df['CMP_TYPE_PARTNER'] = cmp_df['COMPANY_TYPE'].apply(lambda x: 1 if (x == 'PARTNER') else 0)
            cmp_df = cmp_df.drop(columns=['COMPANY_TYPE'], axis=1)

            ret_df = pd.concat([ret_df, cmp_df])

        return ret_df

    @staticmethod
    def _parse_deals(deal_list):
        """
        Создает DataFrame сделок по списку словарей из запроса
        :param deal_list: list of dicts
        :return: pandas.DataFrame
        """

        ret_df = pd.DataFrame(columns=[
                'OPPORTUNITY_DEAL_Q01', 'PROBABILITY_DEAL_Q01', 'TIME_DIFF_BEGIN_CLOSE_DEAL_Q01',
                'OPPORTUNITY_DEAL_Q09', 'PROBABILITY_DEAL_Q09', 'TIME_DIFF_BEGIN_CLOSE_DEAL_Q09',
                'OPPORTUNITY_DEAL_MEAN', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE_DEAL_MEAN', 'CLOSED',
                'OPPORTUNITY_DEAL_MEDIAN', 'TIME_DIFF_BEGIN_CLOSE_DEAL_MEDIAN', 'DEAL_BY_YEAR'])
        ret_df.index.name = 'COMPANY_ID'

        if deal_list:
            deal_df = pd.DataFrame(deal_list)

            deal_df['CLOSED'] = deal_df['CLOSED'].apply(lambda x: 1 if (x == 'Y') else 0)
            deal_df['OPPORTUNITY'] = pd.to_numeric(deal_df['OPPORTUNITY'])
            deal_df['PROBABILITY'] = pd.to_numeric(deal_df['PROBABILITY'])
            deal_df['BEGINDATE'] = pd.to_datetime(deal_df['BEGINDATE'])
            deal_df['CLOSEDATE'] = pd.to_datetime(deal_df['CLOSEDATE'])
            deal_df['TIME_DIFF_BEGIN_CLOSE'] = (deal_df['CLOSEDATE'] - deal_df['BEGINDATE']).astype(
                'timedelta64[h]') / 24

            deal_group = deal_df.groupby(by='COMPANY_ID')

            deal_count = pd.DataFrame(deal_group['CLOSED'].count())
            deal_date_max = deal_group['CLOSEDATE'].max()
            deal_date_min = deal_group['BEGINDATE'].min()
            d = {'YEAR': (deal_date_max - deal_date_min).astype('timedelta64[h]') / (24 * 365)}
            deal_date_max_min_diff = pd.DataFrame(data=d)
            deal_by_year = pd.DataFrame()
            deal_by_year['DEAL_BY_YEAR'] = (deal_count['CLOSED'] / deal_date_max_min_diff['YEAR']).astype(np.float32)
            deal_quantile01 = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE'].quantile(0.1)
            deal_quantile09 = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE'].quantile(0.9)
            deal_mean = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE', 'CLOSED'].mean()
            deal_median = deal_group['OPPORTUNITY', 'TIME_DIFF_BEGIN_CLOSE'].median()

            deal_result = pd.merge(deal_quantile01, deal_quantile09, on='COMPANY_ID',
                                   suffixes=['_DEAL_Q01', '_DEAL_Q09'])
            deal_result1 = pd.merge(deal_mean, deal_median, on='COMPANY_ID', suffixes=['_DEAL_MEAN', '_DEAL_MEDIAN'])
            deal_result = pd.merge(deal_result, deal_result1, on='COMPANY_ID')
            deal_result = pd.merge(deal_result, deal_by_year, on='COMPANY_ID')
            deal_result = deal_result.mask(np.isinf(deal_result))

            ret_df = pd.concat([ret_df, deal_result])

        return ret_df

    @staticmethod
    def _parse_invoices(inv_list):
        """
        Создает DataFrame счетов по списку словарей из запроса
        :param inv_list: list of dicts
        :return: pandas.DataFrame
        """

        ret_df = pd.DataFrame(columns=[
                'PRICE_INV_Q01', 'TIME_DIFF_PAYED_BILL_INV_Q01', 'TIME_DIFF_PAYBEF_PAYED_INV_Q01',
                'PRICE_INV_Q09', 'TIME_DIFF_PAYED_BILL_INV_Q09', 'TIME_DIFF_PAYBEF_PAYED_INV_Q09', 'PRICE_INV_MEAN',
                'TIME_DIFF_PAYED_BILL_INV_MEAN', 'TIME_DIFF_PAYBEF_PAYED_INV_MEAN', 'PAYED', 'STATUS_ID_P',
                'STATUS_ID_D', 'STATUS_ID_N', 'STATUS_ID_T', 'PRICE_INV_MEDIAN', 'TIME_DIFF_PAYED_BILL_INV_MEDIAN',
                'TIME_DIFF_PAYBEF_PAYED_INV_MEDIAN', 'MONTH_TOGETHER_INV', 'DEAL_BY_YEAR'])
        ret_df.index.name = 'UF_COMPANY_ID'

        if inv_list:
            inv_df = pd.DataFrame(inv_list)

            inv_df['PRICE'] = pd.to_numeric(inv_df['PRICE'])
            inv_df['DATE_BILL'] = pd.to_datetime(inv_df['DATE_BILL'])
            inv_df['DATE_PAYED'] = pd.to_datetime(inv_df['DATE_PAYED'])
            inv_df['DATE_PAY_BEFORE'] = pd.to_datetime(inv_df['DATE_PAY_BEFORE'])
            inv_df['TIME_DIFF_PAYED_BILL'] = (inv_df['DATE_PAYED'] - inv_df['DATE_BILL']).astype('timedelta64[h]') / 24
            inv_df['TIME_DIFF_PAYBEF_PAYED'] = (inv_df['DATE_PAY_BEFORE'] - inv_df['DATE_PAYED']).astype('timedelta64[h]') / 24

            inv_df['PAYED'] = inv_df['PAYED'].apply(lambda x: 1 if (x == 'Y') else 0)
            inv_df['STATUS_ID_P'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'P') else 0)
            inv_df['STATUS_ID_D'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'D') else 0)
            inv_df['STATUS_ID_N'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'N') else 0)
            inv_df['STATUS_ID_T'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'T') else 0)

            inv_group = inv_df.groupby(by='UF_COMPANY_ID')

            inv_date_max = inv_group['DATE_PAYED'].max()
            inv_date_min = inv_group['DATE_PAYED'].min()
            inv_month_together = pd.DataFrame()
            inv_month_together['MONTH_TOGETHER_INV'] = (inv_date_max - inv_date_min).astype('timedelta64[h]') / (
                        24 * 30)

            inv_count = pd.DataFrame(inv_group['PAYED'].count())
            inv_by_year = pd.DataFrame(
                data={'DEAL_BY_YEAR': (inv_count['PAYED'] / inv_month_together['MONTH_TOGETHER_INV']) * 12})

            inv_quantile01 = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].quantile(0.1)
            inv_quantile09 = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].quantile(0.9)
            inv_mean = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED', 'PAYED',
                                 'STATUS_ID_P', 'STATUS_ID_D', 'STATUS_ID_N', 'STATUS_ID_T'].mean()
            inv_median = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].median()

            inv_result = pd.merge(inv_quantile01, inv_quantile09, on='UF_COMPANY_ID', suffixes=['_INV_Q01', '_INV_Q09'])
            inv_result1 = pd.merge(inv_mean, inv_median, on='UF_COMPANY_ID', suffixes=['_INV_MEAN', '_INV_MEDIAN'])
            inv_result = pd.merge(inv_result, inv_result1, on='UF_COMPANY_ID')
            inv_result = pd.merge(inv_result, inv_month_together, on='UF_COMPANY_ID')
            inv_result = pd.merge(inv_result, inv_by_year, on='UF_COMPANY_ID')
            inv_result = inv_result.mask(np.isinf(inv_result))

            ret_df = pd.concat([ret_df, inv_result])

        return ret_df

    @staticmethod
    def _parse_quote(quote_list):
        """
        Создает DataFrame коммерческих предложений по списку словарей из запроса
        :param quote_list: list of dicts
        :return: pandas.DataFrame
        """

        ret_df = pd.DataFrame(columns=[
                'OPPORTUNITY_QUO_Q01', 'TIME_DIFF_CREATE_CLOSE_QUO_Q01', 'OPPORTUNITY_QUO_Q09',
                'TIME_DIFF_CREATE_CLOSE_QUO_Q09', 'CLOSED', 'OPPORTUNITY_QUO_MEAN', 'TIME_DIFF_CREATE_CLOSE_QUO_MEAN',
                'STATUS_ID_DEC', 'STATUS_ID_APP', 'STATUS_ID_DRA', 'STATUS_ID_UNA', 'STATUS_ID_REC',
                'OPPORTUNITY_QUO_MEDIAN', 'TIME_DIFF_CREATE_CLOSE_QUO_MEDIAN'])
        ret_df.index.name = 'COMPANY_ID'
        if quote_list:
            quote_df = pd.DataFrame(quote_list)

            quote_df['OPPORTUNITY'] = pd.to_numeric(quote_df['OPPORTUNITY'])
            quote_df['CLOSEDATE'] = pd.to_datetime(quote_df['CLOSEDATE'])
            quote_df['DATE_CREATE'] = pd.to_datetime(quote_df['DATE_CREATE'])
            quote_df['TIME_DIFF_CREATE_CLOSE'] = (quote_df['CLOSEDATE']
                                                  - quote_df['DATE_CREATE']).astype('timedelta64[h]') / 24

            quote_df['CLOSED'] = quote_df['CLOSED'].apply(lambda x: 1 if (x == 'Y') else 0)
            quote_df['STATUS_ID'].value_counts()

            quote_df['STATUS_ID_DEC'] = quote_df['STATUS_ID'].apply(lambda x: 1 if (x == 'DECLAINED') else 0)
            quote_df['STATUS_ID_APP'] = quote_df['STATUS_ID'].apply(lambda x: 1 if (x == 'APPROVED') else 0)
            quote_df['STATUS_ID_DRA'] = quote_df['STATUS_ID'].apply(lambda x: 1 if (x == 'DRAFT') else 0)
            quote_df['STATUS_ID_UNA'] = quote_df['STATUS_ID'].apply(lambda x: 1 if (x == 'UNANSWERED') else 0)
            quote_df['STATUS_ID_REC'] = quote_df['STATUS_ID'].apply(lambda x: 1 if (x == 'RECEIVED') else 0)

            quote_group = quote_df.groupby(by='COMPANY_ID')

            quote_quantile01 = quote_group['OPPORTUNITY', 'TIME_DIFF_CREATE_CLOSE'].quantile(0.1)
            quote_quantile09 = quote_group['OPPORTUNITY', 'TIME_DIFF_CREATE_CLOSE'].quantile(0.9)
            quote_mean = quote_group['CLOSED', 'OPPORTUNITY', 'TIME_DIFF_CREATE_CLOSE', 'STATUS_ID_DEC',
                                     'STATUS_ID_APP', 'STATUS_ID_DRA', 'STATUS_ID_UNA', 'STATUS_ID_REC'].mean()
            quote_median = quote_group['OPPORTUNITY', 'TIME_DIFF_CREATE_CLOSE'].median()

            quo_result = pd.merge(quote_quantile01, quote_quantile09, on='COMPANY_ID',
                                  suffixes=['_QUO_Q01', '_QUO_Q09'])
            quo_result1 = pd.merge(quote_mean, quote_median, on='COMPANY_ID', suffixes=['_QUO_MEAN', '_QUO_MEDIAN'])
            quo_result = pd.merge(quo_result, quo_result1, on='COMPANY_ID')
            quo_result = quo_result.mask(np.isinf(quo_result))

            ret_df = pd.concat([ret_df, quo_result])

        return ret_df

    @staticmethod
    def get_data_frame(cmp_list, deal_list, inv_list, quote_list):
        """
        Формирует DataFrame по деятельности компаний
        :param cmp_list: list of dicts
        :param deal_list: list of dicts
        :param inv_list: list of dicts
        :param quote_list: list of dicts
        :return: pandas.DataFrame
        """
        cmp_df = DataParser._parse_companies(cmp_list)
        deal_df = DataParser._parse_deals(deal_list)
        inv_df = DataParser._parse_invoices(inv_list)
        quote_df = DataParser._parse_quote(quote_list)

        result = pd.merge(cmp_df, deal_df, left_on='ID', right_on='COMPANY_ID', suffixes=('CMP', 'DEALS'), how='outer')
        if 'COMPANY_ID' in result.columns.values:
            result = result.drop(columns=['COMPANY_ID'], axis=1)

        result = pd.merge(result, inv_df, left_on='ID', right_on='UF_COMPANY_ID', suffixes=('', 'INV'), how='outer')
        if 'UF_COMPANY_ID' in result.columns.values:
            result = result.drop(columns=['UF_COMPANY_ID'], axis=1)

        result = pd.merge(result, quote_df, left_on='ID', right_on='COMPANY_ID', suffixes=('', 'QUO'), how='outer')
        if 'COMPANY_ID' in result.columns.values:
            result = result.drop(columns=['COMPANY_ID'], axis=1)

        result = result.set_index('ID')

        result = result.fillna(0)

        return result
