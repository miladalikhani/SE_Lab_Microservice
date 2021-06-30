import json
from flask import Flask, abort,request,jsonify
import requests

app = Flask(__name__)

@app.route('/api/view_profile')
def view_profile():
    headers = request.headers
    if 'username' not in headers:
        abort(406)
    else:
        username = headers['username']
        res = {'username': username}
        return res


@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(port=8082)