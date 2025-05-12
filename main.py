from flask import Flask, request, jsonify, make_response, redirect
from db import Database
from auth import Auth
import random
import string
from flask import Flask, render_template

app = Flask(__name__)
db_path = "urls.db"
db = Database(db_path)
auth = Auth()


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def create_cookie_session(user_name, password):
    session = auth.login(user_name, password)
    resp = make_response(jsonify({'message': 'ok'}))
    resp.set_cookie('session_id', session, max_age=60 * 60 * 7)
    return resp


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'pong': 'pong!'})


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')
    if not user_name or not password:
        return jsonify({'error': 'Missing user_name or password'}), 400

    if db.user_exists(user_name):
        return jsonify({'error': 'Username already exists'}), 400

    db.save_user(user_name, password)

    return create_cookie_session(user_name, password), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')
    if not user_name or not password:
        return jsonify({'error': 'Missing user_name or password'}), 400

    if not db.check_user_and_password(user_name, password):
        return jsonify({'error': 'Username or password is incorrect'}), 400

    return create_cookie_session(user_name, password), 200


@app.route('/saveUrl', methods=['POST'])
def saveUrl():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({'error': 'Unauthorized'}), 401
    if not auth.check_session(session_id):
        return jsonify({'error': 'Invalid session'}), 401

    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400
    short_url = generate_short_url()
    db.save_short_long_urls(short_url, url)
    return jsonify({'short_url': short_url, 'original_url': url})


@app.route('/<short_url>')
def redirect_short_url(short_url):
    long_url = db.get_long_url(short_url)
    if not long_url:
        return jsonify({'error': 'No long url found'}), 404
    return redirect(long_url)


@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')


@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/shortener')
def shortener():
    return render_template('shortener.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
