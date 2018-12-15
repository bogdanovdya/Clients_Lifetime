from app import app, db
from flask import render_template, request
from installApplication import InstallApplication
from indexApplication import IndexApplication
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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/install', methods=['GET', 'POST'])
def install():
    install_app = InstallApplication(**get_post())
    install_app.create_bot()
    return render_template('install.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    index_app = IndexApplication(**get_post())
    cmp_ids = index_app.get_cmp_ids()

    if cmp_ids is not None:
        call = index_app.get_companies(cmp_ids)
        return render_template('index.html', domain=index_app.domain, lang=index_app.lang,
                               auth_token=index_app.auth_token, ref_token=index_app.ref_token, companies=call)
    else:
        return render_template('index.html', companies=[{'ID': 0, 'TITLE': 'Ничего не найдено'}])


@app.route('/model_predict', methods=['GET', 'POST'])
def get_result():
    index_app = IndexApplication(**get_post())
    cmp_list = request.values.getlist('companies')
    data = index_app.get_data(cmp_list)
    data_frame = DataParser.get_data_frame(**data)
    predict = Predictor(data_frame).make_predict()

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

    if 'event' in data:
        event = data['event']
        domain = data['auth[domain]'].split('.bitrix24.')[0]
        lang = data['auth[domain]'].split('.bitrix24.')[1]

        auth_info = PortalAuth.query.filter_by(portal=domain).first()
        bot_app = BotApplication(domain, lang, auth_info.access_token, auth_info.refresh_token)

        if event == 'ONIMBOTMESSAGEADD':
            in_message = data['data[PARAMS][MESSAGE]']
            chat_id = data['data[PARAMS][FROM_USER_ID]']
            check = bot_app.check_message(in_message)

            if check['command'] == '/about':
                bot_app.send_about(chat_id=chat_id)

            elif check['command'] == '/search':
                bot_app.get_company_by_title(check['content'], chat_id=chat_id)

            elif check['command'] == '/cmp':
                index_app = IndexApplication(domain, lang, auth_info.access_token, auth_info.refresh_token)
                data = index_app.get_data(check['content'])
                data_frame = DataParser.get_data_frame(data[0], data[1], data[2], data[3])
                predict = Predictor(data_frame).make_predict()
                message = ''
                for item in predict:
                    message += 'Вероятность для компании ' + item['TITLE'] + ' -- ' + str(item['PREDICT'])
                bot_app.send_message(chat_id=chat_id, message=message)

            else:
                bot_app.send_message(chat_id=chat_id,
                                     message='Привет, ' + data['data[USER][FIRST_NAME]'] + ' '
                                             + data['data[USER][LAST_NAME]'] + '!')
                bot_app.send_keyboard(chat_id=chat_id)

        else:
            auth_info.event_counter += 1
            db.session.commit()
            if auth_info.event_counter >= 10:
                bot_app.send_message(message='Произошло много изменений, пора пересчитать предсказания')
                bot_app.send_keyboard()
                auth_info.event_counter = 0
                db.session.commit()

    return 'true'
