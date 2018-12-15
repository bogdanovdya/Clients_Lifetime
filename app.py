from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ssl
from app_settings import AppSetting


context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert/ia.crt', 'cert/ia.key')

app = Flask(__name__)
app.config.from_object(AppSetting)

db = SQLAlchemy(app)