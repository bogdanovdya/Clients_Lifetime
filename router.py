from bottle import route, run, template


@route('/install')
def install():
    return template('install')


@route('/index')
def index():
    return template('index')


if __name__ == '__main__':
    run(debug=True, reloader=True)
