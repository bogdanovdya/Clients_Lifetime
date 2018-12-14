from bitrix24.bitrix24 import Bitrix24


class BotApplication:
    def __init__(self, domain, lang, auth_token, ref_token):
        self.domain = domain
        self.auth_token = auth_token
        self.lang = lang
        self.ref_token = ref_token
        self.bx24 = Bitrix24(domain=self.domain, auth_token=self.auth_token,
                             refresh_token=self.ref_token, high_level_domain=self.lang)

    def send_message(self, chat_id=1, message='Привет!', attach='', keyboard='', menu=''):
        """
        Отправка сообщения от чат-бота
        :param chat_id: Идентификатор диалога, это либо USER_ID пользователя, либо chatXX - где XX идентификатор чата,
                        передается в событии ONIMBOTMESSAGEADD и ONIMJOINCHAT
        :param message: Тест сообщения
        :param attach: Вложение, необязательное поле
        :param keyboard: Клавиатура, необязательное поле
        :param menu: Контекстное меню, необязательное поле
        :return:
        """
        self.bx24.call('imbot.message.add',
                       {
                           'DIALOG_ID': chat_id,
                           'MESSAGE': message,
                           'ATTACH': attach,
                           'KEYBOARD': keyboard,
                           'MENU': menu
                       })
