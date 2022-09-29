import os, time, requests
from flask import Flask, jsonify
from requests.auth import HTTPDigestAuth
from flask_httpauth import HTTPDigestAuth as flaskauth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = flaskauth()

default = {
    "vcu": "rams"
}


def to_json(time):
    json_post = {
        'pingpong_t': time*1000
    }
    return json_post


@auth.get_password
def check_pw(usr):
    if usr in default:
        return default.get(usr)
    return None


@app.route('/ping', methods=['GET'])
@auth.login_required
def ping_get():
    url = 'http://127.0.0.1:5001/'
    start = time.time()
    r = requests.get(url + 'pong', auth=HTTPDigestAuth('vcu', 'rams'))
    end = time.time()
    return jsonify(to_json(end - start)), 201


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'Page Not Here'}), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message':'Something is Broke'}), 500
