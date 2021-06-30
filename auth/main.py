import json
from flask import Flask, abort, request, make_response, jsonify
import requests
import jwt

secret_key = "very_secret"

app = Flask(__name__)


def get_all_users():
    auth_users_file = open("auth_users.json")
    auth_users = json.load(auth_users_file)
    auth_users_file.close()
    return auth_users


def check_user(username, password):
    auth_users = get_all_users()
    for entity in auth_users['users']:
        if entity['username'] == username:
            if entity['password'] == password:
                return True
            else:
                return False
    return False


@app.route("/auth/login", methods=['POST'])
def login():
    if not request.json:
        abort(401)
    user_data = request.json
    if not user_data.get('username') or not user_data.get('password'):
        abort(401)
    username = user_data.get('username')
    password = user_data.get('password')
    status = check_user(username, password)
    if (status):
        token = jwt.encode(
            payload={"username": username},
            key=secret_key,
            algorithm="HS256"
        )
        response = make_response(jsonify({}))
        response.headers['token'] = token
        return response
    else:
        abort(401)


@app.route("/auth/authenticate")
def authenticate():
    if 'token' not in request.headers:
        abort(401)
    token = request.headers['token']
    try:
        data = jwt.decode(
            jwt=token,
            key=secret_key,
            algorithms=["HS256"]
        )
    except:
        abort(401)
    if 'username' not in data:
        abort(401)
    return jsonify({"username": data['username']}), 200


if __name__ == '__main__':
    app.run(port=8081)
