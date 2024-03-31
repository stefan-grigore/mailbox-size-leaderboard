import json

from flask import request, jsonify

from models.token import Token
from models.user import User


def get_current_user():
    token = get_token_from_request()
    if not token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    # Find user by userId from the token
    user = User.objects(id=token.userId).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user = json.loads(user.to_json())
    del user['password']

    return jsonify(user), 200


def get_token_from_request():
    token_value = request.cookies.get('token')
    token = Token.objects(tokenValue=token_value).first()
    return token


def update_current_user():
    try:
        # Extract token from cookies or authorization header
        token_value = request.cookies.get('token')
        # Find token document
        token = Token.objects(tokenValue=token_value).first()
        if not token:
            return jsonify({'error': 'Invalid or missing token'}), 401

        # Find user by userId from the token
        user = User.objects(id=token.userId).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Extract data from request
        data = request.json
        username = data.get('username')
        mailbox_size = data.get('mailboxSize')
        mailbox_unit = data.get('mailboxUnit')

        # Update the user document
        if username:
            user.username = username
        if mailbox_size is not None:
            user.mailboxSize = mailbox_size
        if mailbox_unit:
            user.mailboxUnit = mailbox_unit
        user.save()

        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Error updating user: {}'.format(str(e))}), 500
