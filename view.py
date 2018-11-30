from app import app
from flask import render_template, request
from installApplication import InstallApplication
from indexApplicaton import Application


def get_post():
    domain = request.values.get('DOMAIN')
    lang = request.values.get('LANG')
    auth_token = request.values.get('AUTH_ID')
    ref_token = request.values.get('REFRESH_ID')
    return {'domain': domain, 'lang': lang, 'auth_token': auth_token, 'ref_token': ref_token}


@app.route('/install', methods=['GET', 'POST'])
def install():
    try:
        post_data = get_post()
        install_app = InstallApplication(**post_data)
        install_app.save_auth()
    finally:
        return render_template('install.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        post_data = get_post()
        bx24 = Application(**post_data)
        bx24.save_auth()
        call = bx24.get_data()
    except Exception:
        return render_template('conn_err.html')
    else:
        return render_template('index.html', domain=bx24.domain, lang=bx24.lang,
                               auth_token=bx24.auth_token, ref_token=bx24.ref_token, companies=call)


@app.route('/model_predict', methods=['GET', 'POST'])
def get_result():
    try:
        auth_data = get_post()
        bx24 = Application(**auth_data)
        bx24.save_auth()
    except Exception:
        return render_template('conn_err.html')
    else:
        return render_template('model_predict.html')
