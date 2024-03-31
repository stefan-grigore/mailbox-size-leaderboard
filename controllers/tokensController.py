import json
import uuid
from flask import jsonify, request

from models.token import Token
from models.user import User


def token_is_valid():
    token = request.headers.get('Authorization')
    if 'token' not in request.cookies and token is None:
        return False
    if token is None:
        token = request.cookies['token']
    else:
        token = token.replace('Bearer ', '')
    token = Token.objects(tokenValue=token).first()
    if not token:
        return False
    return True


def create_token(bcrypt):
    try:
        data = request.json
        username = data['username']
        password = data['password']

        user = User.objects(username=username).first()
        if not user:
            return 'Unauthorized', 401

        if not bcrypt.check_password_hash(user.password, password):
            return 'Unauthorized', 401

        token = Token(
            userId=str(user.id),
            tokenValue=str(uuid.uuid4())
        ).save()

        return jsonify(json.loads(token.to_json())), 200

    except Exception as error:
        print(error)
        return 'Error generating token', 500
