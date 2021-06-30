import json
from flask import Flask, abort,request,make_response,jsonify
import requests

app = Flask(__name__)

endpoints = []



@app.before_first_request
def load_endpoints():
    endpoints_file = open('endpoints.json')
    data = json.load(endpoints_file)
    endpoints_file.close()
    global endpoints
    endpoints = data


def send_request(endpoint, headers):
    if request.method == 'GET':
        res = requests.get(endpoint, headers=headers)
        return res
    elif request.method == 'POST':
        res = requests.post(endpoint, headers=headers)
        return res

@app.route('/')
def hello():
    return "hello world"


@app.route('/<path:path>', methods=['GET', 'POST'])
def gateway(path):
    global endpoints
    if path in endpoints:
        endpoint = endpoints[path]
        headers = {}
        for k,v in request.headers:
            headers[k] = v
        response = send_request(endpoint, headers)
        if response.status_code not in [200, 201]:
            abort(response.status_code)
        return jsonify(response.json())
    else:
        abort(404)


if __name__ == '__main__':
    app.run(port=8080)
