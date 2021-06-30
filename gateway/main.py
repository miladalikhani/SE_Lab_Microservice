import json

from flask import Flask, abort

app = Flask(__name__)

endpoints = []


@app.before_first_request
def load_endpoints():
    endpoints_file = open('endpoints.json')
    data = json.load(endpoints_file)
    endpoints_file.close()
    global endpoints
    endpoints = data


@app.route('/')
def hello():
    return "hello world"


@app.route('/<path:path>', methods=['GET', 'POST'])
def gateway(path):
    global endpoints
    if path in endpoints:
        return endpoints[path]
    else:
        abort(404)


if __name__ == '__main__':
    app.run(port=8080)
