from app_settings import Bitrix24Setting
from IApplication import *


class InstallApplication(IApplication):

    def create_bot(self):
        """
        Создает на портале бота и привязывает вебхук
        :return:
        """
        self.bx24.call('imbot.register',
                       {
                           'CODE': 'datascientist',
                           'TYPE': 'H',
                           'EVENT_HANDLER': Bitrix24Setting.bot_url,
                           'PROPERTIES': {
                               'NAME': 'Ваня',
                               'LAST_NAME': 'Аналитик',
                               'COLOR': 'blue',
                               'WORK_POSITION': 'data scientist'
                           }
                       })

    def create_webhooks(self):
        """
        Создает на портале вебхуки связанные с обновлениями сделок и счетов
        :return:
        """
        self.bx24.call('event.bind', {'event': 'ONCRMINVOICEADD'}, {'handler': Bitrix24Setting.bot_url})
        self.bx24.call('event.bind', {'event': 'ONCRMINVOICEUPDATE'}, {'handler': Bitrix24Setting.bot_url})
        self.bx24.call('event.bind', {'event': 'ONCRMDEALADD'}, {'handler': Bitrix24Setting.bot_url})
        self.bx24.call('event.bind', {'event': 'ONCRMDEALUPDATE'}, {'handler': Bitrix24Setting.bot_url})
