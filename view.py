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
        install_app = InstallApplication(**get_post())
        install_app.save_auth()
    finally:
        return render_template('install.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():

    bx24 = Application(**get_post())
    bx24.save_auth()
    cmp_ids = bx24.get_cmp_ids()
    call = bx24.get_companies(cmp_ids)

    return render_template('index.html', domain=bx24.domain, lang=bx24.lang,
                           auth_token=bx24.auth_token, ref_token=bx24.ref_token, companies=call)


@app.route('/model_predict', methods=['GET', 'POST'])
def get_result():
    try:
        bx24 = Application(**get_post())
        bx24.save_auth()
        cmp_list = request.values.getlist('companies')
        data = bx24.get_data(cmp_list)
    except Exception:
        return render_template('conn_err.html')
    else:
        return render_template('model_predict.html', companies=cmp_list, data=data)
