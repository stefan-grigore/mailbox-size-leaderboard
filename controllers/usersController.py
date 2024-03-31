import json

from flask import jsonify, request

from controllers import tokensController
from models.user import User


def get_users():
    users = User.objects.all()
    return jsonify(json.loads(users.to_json())), 200


def create_user(bcrypt):
    try:
        data = request.json
        username = data['username']
        password = data['password']
        mailbox_size = data['mailboxSize']
        mailbox_unit = data['mailboxUnit']

        existing_user = User.objects(username=username).first()
        if existing_user:
            return jsonify({'error': 'A user with that username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        User(
            username=username,
            password=hashed_password,
            mailboxSize=mailbox_size,
            mailboxUnit=mailbox_unit
        ).save()

        return tokensController.create_token(bcrypt)

    except Exception as error:
        print(error)
        return jsonify({'error': 'Error creating user'}), 500
