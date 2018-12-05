import pandas as pd


class ParserFromApp:
    """
    TODO парсер из приложения
    """
    def parse_companies(self, cmp_list):
        cmp_df = pd.DataFrame(cmp_list)
        cmp_df = cmp_df.drop_duplicates('ID')
        return cmp_df

    def parce_deals(self, deal_list):
        deal_df = pd.DataFrame(deal_list)

        deal_df['CLOSED'] = deal_df['CLOSED'].apply(lambda x: 1 if (x == 'Y') else 0)
        deal_df['BEGINDATE'] = pd.to_datetime(deal_df['BEGINDATE'])
        deal_df['CLOSEDATE'] = pd.to_datetime(deal_df['CLOSEDATE'])
        deal_df['TIME_DIFF_BEGIN_CLOSE'] = (deal_df['CLOSEDATE'] - deal_df['BEGINDATE']).astype('timedelta64[h]') / 24

        deal_group = deal_df.groupby(by='COMPANY_ID')

        deal_quantile01 = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE'].quantile(0.1)
        deal_quantile09 = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE'].quantile(0.9)
        deal_mean = deal_group['OPPORTUNITY', 'PROBABILITY', 'TIME_DIFF_BEGIN_CLOSE', 'CLOSED'].mean()
        deal_median = deal_group['OPPORTUNITY', 'TIME_DIFF_BEGIN_CLOSE'].median()

        deal_result = pd.merge(deal_quantile01, deal_quantile09, on='COMPANY_ID', suffixes=['_DEAL_Q01', '_DEAL_Q09'])
        deal_result1 = pd.merge(deal_mean, deal_median, on='COMPANY_ID', suffixes=['_DEAL_MEAN', '_DEAL_MEDIAN'])
        deal_result = pd.merge(deal_result, deal_result1, on='COMPANY_ID')

        return deal_result

    def parse_invoices(self, inv_list):
        inv_df = pd.DataFrame(inv_list)

        inv_df['DATE_BILL'] = pd.to_datetime(inv_df['DATE_BILL'])
        inv_df['DATE_PAYED'] = pd.to_datetime(inv_df['DATE_PAYED'])
        inv_df['DATE_PAY_BEFORE'] = pd.to_datetime(inv_df['DATE_PAY_BEFORE'])
        inv_df['TIME_DIFF_PAYED_BILL'] = (inv_df['DATE_PAYED']
                                          - inv_df['DATE_BILL']).astype('timedelta64[h]') / 24
        inv_df['TIME_DIFF_PAYBEF_PAYED'] = (inv_df['DATE_PAY_BEFORE']
                                            - inv_df['DATE_PAYED']).astype('timedelta64[h]') / 24

        inv_df['PAYED'] = inv_df['PAYED'].apply(lambda x: 1 if (x == 'Y') else 0)
        inv_df['STATUS_ID_P'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'P') else 0)
        inv_df['STATUS_ID_D'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'D') else 0)
        inv_df['STATUS_ID_N'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'N') else 0)
        inv_df['STATUS_ID_T'] = inv_df['STATUS_ID'].apply(lambda x: 1 if (x == 'T') else 0)

        inv_group = inv_df.groupby(by='UF_COMPANY_ID')

        inv_quantile01 = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].quantile(0.1)
        inv_quantile09 = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].quantile(0.9)
        inv_mean = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED', 'PAYED',
                             'STATUS_ID_P', 'STATUS_ID_D', 'STATUS_ID_N', 'STATUS_ID_T'].mean()
        inv_median = inv_group['PRICE', 'TIME_DIFF_PAYED_BILL', 'TIME_DIFF_PAYBEF_PAYED'].median()

        inv_result = pd.merge(inv_quantile01, inv_quantile09, on='UF_COMPANY_ID', suffixes=['_INV_Q01', '_INV_Q09'])
        inv_result1 = pd.merge(inv_mean, inv_median, on='UF_COMPANY_ID', suffixes=['_INV_MEAN', '_INV_MEDIAN'])
        inv_result = pd.merge(inv_result, inv_result1, on='UF_COMPANY_ID')

        return inv_result


class ParserFromModel:
    """
    TODO парсер из модели(да и саму модель)
    """