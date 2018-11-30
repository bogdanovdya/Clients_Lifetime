from flask import Flask
import ssl
from app_settings import RouterSetting

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert/ia.crt', 'cert/ia.key')

app = Flask(__name__)
app.config.from_object(RouterSetting)

