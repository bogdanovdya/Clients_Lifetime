from bitrix24.bitrix24 import Bitrix24
from models import PortalAuth
from app import db
from app_settings import Bitrix24Setting


class InstallApplication:
    def __init__(self, domain, lang, auth_token, ref_token):
        self.domain = domain.split('.bitrix24')[0]
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = ref_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)
        self.save_auth()

    def save_auth(self):
        """
        Сохраняет данные OAuth в БД
        :return:
        """
        portal_auth = PortalAuth.query.filter_by(portal=self.domain).first()

        if portal_auth is not None:
            portal_auth.access_token = self.auth_token
            portal_auth.refresh_token = self.ref_token
        else:
            portal_auth = PortalAuth(portal=self.domain, access_token=self.auth_token, refresh_token=self.ref_token)
            db.session.add(portal_auth)

        db.session.commit()

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
