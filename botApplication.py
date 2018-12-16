from IApplication import *


class BotApplication(IApplication):

    def send_message(self, chat_id=1, message='Привет!'):
        """
        Отправка сообщения от чат-бота
        :param chat_id: user or chat ID
        :param message: message text
        :return: message in chat
        """
        self.bx24.call('imbot.message.add',
                       {
                           'DIALOG_ID': chat_id,
                           'MESSAGE': message,
                       })

    def send_keyboard(self, chat_id=1):
        """
        Отправляет сообщение с командами для пользователя
        :param chat_id: user or chat ID
        :return: message in chat
        """
        self.bx24.call('imbot.message.add', {'DIALOG_ID': chat_id},
                       {
                           'MESSAGE': '[send=/about]Обо мне[/send] [br] '
                                      '[put=/search]Найти компанию[/put]'

                       })

    def send_about(self, chat_id=1):
        """
        Отправялет сообщение с информацией о боте
        :param chat_id: user or chat ID
        :return: message in chat
        """
        self.bx24.call('imbot.message.add',
                       {
                           'DIALOG_ID': chat_id,
                           'MESSAGE': 'Привет! Я занимаюсь анализом данных в вашей компании - '
                                      'прогнозирую с какими клиентами стоит иметь дело. Ты можешь обратиться ко мне '
                                      'здесь или воспользоваться приложением. Если ты очень долго не будешь заходить '
                                      'в приложение за прогнозом, я напомню тебе в чате. [br]'
                                      '[put=/search]Найти компанию[/put]'
                       })

    def check_message(self, message):
        """
        Парсит сообщение на комманды, если есть
        :param message: input message
        :return: command and content
        """
        if message[0] == '/':
            command = message.split(' ')[0]
            content = message.split(command)[1][1:]
            return {'command': command, 'content': content}
        else:
            return {'command': '', 'content': message}

    def get_company_by_title(self, title, chat_id=1):
        """
        Ищет подхоящие комании по названию
        :param title: company title
        :param chat_id: user or chat ID
        :return: message in chat
        """
        call = self.bx24.call('crm.company.list', {'FILTER': {'>=TITLE': title}},
                              {'SELECT': ['ID', 'TITLE']})
        result = call['result']
        message = ''
        for item in result:
            message += '[send=/cmp '+item['ID']+']'+item['ID']+'. '+item['TITLE']+'[/send] [br] '

        self.bx24.call('imbot.message.add', {'DIALOG_ID': chat_id}, {'MESSAGE': message})
