from bitrix24.bitrix24 import Bitrix24
from bx24_tools.bx24_connect import *
from bx24_tools.db_connect import *


class Application:
    """
    TO DO проверка логина, отправка батча
    """
    def __init__(self):
        self.ar_access_params = ()
        self.b24_error = None
        self.is_background_mode = False
        self.ar_b24_apps = None

    def check_b24_auth(self):
        """
        :return: Успешность/класс ошибки
        """
        is_tocken_refreshed = False
        try:
            self.ar_b24_apps = Bitrix24()
            self.b24_error = True
        except ValueError:
            self.b24_error = ValueError
        except TypeError:
            self.b24_error = TypeError
        except Exception:
            self.b24_error = Exception
        return self.b24_error