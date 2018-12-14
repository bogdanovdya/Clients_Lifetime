from app import app, db
from flask import render_template, request
from installApplication import InstallApplication
from indexApplicaton import IndexApplication
from botApplication import BotApplication
from model.data_parser import DataParser
from model.predictor import Predictor
from models import PortalAuth


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
        install_app.create_bot()

    except Exception:
        render_template('conn_err.html')

    else:
        return render_template('install.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        index_app = IndexApplication(**get_post())
        cmp_ids = index_app.get_cmp_ids()

    except Exception:
        return render_template('conn_err.html')

    else:
        if cmp_ids is not None:
            call = index_app.get_companies(cmp_ids)
            return render_template('index.html', domain=index_app.domain, lang=index_app.lang,
                                   auth_token=index_app.auth_token, ref_token=index_app.ref_token, companies=call)
        else:
            return render_template('index.html', companies=[{'ID': 0, 'TITLE': 'Ничего не найдено'}])


@app.route('/model_predict', methods=['GET', 'POST'])
def get_result():
    try:
        index_app = IndexApplication(**get_post())
        cmp_list = request.values.getlist('companies')
        data = index_app.get_data(cmp_list)
        data_frame = DataParser.get_data_frame(data[0], data[1], data[2], data[3])
        predict = Predictor(data_frame).make_predict()

    except Exception:
        return render_template('conn_err.html')

    else:
        if request.values.get('return_type') == 'frame':
            return render_template('model_predict.html', data=predict)

        if request.values.get('return_type') == 'chat':
            for item in predict:
                message = 'Вероятность для компании ' + item['TITLE'] + ' -- ' + str(item['PREDICT'])
                index_app.send_message(title=item['TITLE'], content=message)
            return render_template('index.html')


@app.route('/bot', methods=['GET', 'POST'])
def bot_message():
    data = request.values.to_dict()
    print('---------------------------------------------------------------------------------------------------------')
    print(data)
    print('---------------------------------------------------------------------------------------------------------')
    if 'event' in data:
        event = data['event']
        domain = data['auth[domain]'].split('.bitrix24.')[0]
        lang = data['auth[domain]'].split('.bitrix24.')[1]

        auth_info = PortalAuth.query.filter_by(portal=domain).first()
        bot_app = BotApplication(domain, lang, auth_info.access_token, auth_info.refresh_token)

        if event == 'ONIMBOTMESSAGEADD':
            chat_id = data['data[PARAMS][FROM_USER_ID]']
            bot_app.send_message(chat_id=chat_id)

        elif event == 'ONCRMINVOICEUPDATE':
            auth_info.event_counter += 1
            db.session.commit()


    return 'true'

