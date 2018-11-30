from app import app, context
import view

if __name__ == '__main__':
    app.run(ssl_context=context, port=443, host='0.0.0.0')
