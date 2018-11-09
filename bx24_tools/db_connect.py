"""тут будет коннект к бд"""
class DBConnect:
    def save_auth(self, domain, token, refresh_token, member_id):
        self.querry = 'INSERT INTO b24_portal_reg (`PORTAL`, `ACCESS_TOKEN`, `REFRESH_TOKEN`, `MEMBER_ID`) ' \
                      'values ({0}, {1}, {2}, {3}) ON DUPLICATE ' \
                      'KEY UPDATE `ACCESS_TOKEN` = {1}, `REFRESH_TOKEN` = {2}, `MEMBER_ID` = {3}'\
            .format(domain, token, refresh_token, member_id)
