from flask import Flask
from data import __all_models
from data.db_session import global_init
from data.users import User
from blueprint.auth import auth_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def main():
    global_init('main.db')
    app.register_blueprint(auth_bp)
    app.run(port=5000, host='127.0.0.1', debug=True)

if __name__ == '__main__':
    main()