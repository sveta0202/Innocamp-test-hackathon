from flask import Flask, redirect, url_for, session

from data import __all_models
from data.db_session import global_init
from blueprint.auth import auth_bp
from blueprint.calendar import calendar_bp
from blueprint.events import events_bp

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/')
def index():
    if session.get('user_id'):
        return redirect(url_for('calendar_bp.index'))
    return redirect(url_for('auth.login'))


def main():
    global_init('main.db')
    app.register_blueprint(auth_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(events_bp)
    app.run(port=5000, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()