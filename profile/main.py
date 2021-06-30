import json
from flask import Flask, abort,request,jsonify, make_response


app = Flask(__name__)

def get_all_profiles():
    users_profile_file = open("user_profile.json")
    users_profile = json.load(users_profile_file)
    users_profile_file.close()
    return users_profile


def get_user_profile(username):
    users = get_all_profiles()
    for entity in users['users']:
        if entity['username'] == username:
            return True, entity
    return False, {}



@app.route('/api/view_profile')
def view_profile():
    headers = request.headers
    if 'username' not in headers:
        abort(401)
    else:
        username = headers['username']
        profile = get_user_profile(username)
        if not profile[0]:
            abort(406)
        else:
            res = make_response(jsonify(profile[1]))
            if 'token' in request.headers:
                res.headers['token'] = request.headers['token']
            return res

@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(port=8082)