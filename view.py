from app import app
from flask import render_template, request
from installApplication import InstallApplication
from indexApplicaton import Application
from model.data_parser import DataParser
from model.predictor import Predictor


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
    except Exception:
        render_template('conn_err.html')
    else:
        return render_template('install.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        bx24 = Application(**get_post())
        bx24.save_auth()
        cmp_ids = bx24.get_cmp_ids()
    except Exception:
        return render_template('conn_err.html')
    else:
        if cmp_ids is not None:
            call = bx24.get_companies(cmp_ids)
            return render_template('index.html', domain=bx24.domain, lang=bx24.lang,
                                   auth_token=bx24.auth_token, ref_token=bx24.ref_token, companies=call)
        else:
            return render_template('index.html', companies=[{'ID': 0, 'TITLE': 'Ничего не найдено'}])

        '''
        чтоб все получить, пусть побудет здесь
                if cmp_ids is not None:
                    call_res = []
                    for id in cmp_ids:
                        call = bx24.get_companies(id)
                        if call:
                            call_res.extend(call)
                    return render_template('index.html', domain=bx24.domain, lang=bx24.lang,
                                   auth_token=bx24.auth_token, ref_token=bx24.ref_token, companies=call_res)
                else:
                    return render_template('index.html', companies=[{'ID': 0, 'TITLE': 'Ничего не найдено'}])
        '''


@app.route('/model_predict', methods=['GET', 'POST'])
def get_result():
    bx24 = Application(**get_post())
    bx24.save_auth()
    cmp_list = request.values.getlist('companies')
    data = bx24.get_data(cmp_list)
    data_frame = DataParser.get_data_frame(data[0], data[1], data[2], data[3])
    predict = Predictor(data_frame).make_predict()

    return render_template('model_predict.html', companies=cmp_list, data=predict)
