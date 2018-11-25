from flask import Flask, render_template, request
from Application import Application
import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('cert/ia.crt', 'cert/ia.key')

app = Flask(__name__)


@app.route('/install', methods=['GET', 'POST'])
def install():
    try:
        domain = request.values.get('DOMAIN')
        lang = request.values.get('LANG')
        auth_token = request.values.get('AUTH_ID')
        ref_token = request.values.get('REFRESH_ID')
        bx24 = Application(domain, lang, auth_token, ref_token)
        bx24.save_auth()
    finally:
        return render_template('install.tpl')


@app.route('/index', methods=['POST'])
def get_data():
    try:
        domain = request.values.get('DOMAIN')
        lang = request.values.get('LANG')
        auth_token = request.values.get('AUTH_ID')
        ref_token = request.values.get('REFRESH_ID')
        bx24 = Application(domain, lang, auth_token, ref_token)
        bx24.save_auth()
    finally:
        return render_template('index.tpl', domain=domain, lang=lang,
                               auth_token=auth_token, ref_token=ref_token)


if __name__ == "__main__":
    app.run(ssl_context=context, host='0.0.0.0')
