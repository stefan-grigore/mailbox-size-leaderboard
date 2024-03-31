import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine

from controllers import tokensController, usersController, currentUserController

load_dotenv()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('DB_NAME', 'mailbox-size-leaderboard'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '27017'))
}
db = MongoEngine(app)
bcrypt = Bcrypt(app)


@app.route('/api/users', methods=['GET'])
def get_users():
    if not tokensController.token_is_valid():
        return render_template("login.html"), 401
    return usersController.get_users()


@app.route('/api/users', methods=['POST'])
def create_user():
    return usersController.create_user(bcrypt)


@app.route('/api/current-user', methods=['GET'])
def get_current_user():
    if not tokensController.token_is_valid():
        return render_template("login.html"), 401
    return currentUserController.get_current_user()


@app.route('/api/current-user', methods=['PUT'])
def update_current_user():
    if not tokensController.token_is_valid():
        return render_template("login.html"), 401
    return currentUserController.update_current_user()


@app.route('/api/token', methods=['POST'])
def create_token():
    return tokensController.create_token(bcrypt)


@app.route('/')
def index():
    if not tokensController.token_is_valid():
        return render_template("login.html"), 401
    return render_template('index.html')


if __name__ == '__main__':
    try:
        port = os.getenv('PORT', 3000)
        debug = os.getenv('DEBUG', True)
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        print(f"Error starting server: {e}")
