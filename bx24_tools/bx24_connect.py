"""тут будет коннект к битриксу"""
from bitrix24.bitrix24 import Bitrix24


class B24Connect:
    @staticmethod
    def auth(domain, token):
        """
        :return:
        """
        is_token_refreshed = False
        try:
            b24_app = Bitrix24(domain=domain, auth_token=token)
            b24_error = False
        except ValueError:
            b24_error = ValueError
        except TypeError:
            b24_error = TypeError
        except Exception:
            b24_error = Exception
        finally:
            return {'err': b24_error, 'app': b24_app}
