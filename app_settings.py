import os
"""change this for yourself"""


class Bitrix24Setting(object):
    app_id = 'local.5bf96bc48f8048.50744254'
    app_secret_code = '5e1jtZAuY70N1j2RAlUUUJaxoGU482t47sv6ZTNn4PXbz7L1Pi'
    app_reg_url = ''


class AppSetting(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/clients_lifetime'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
