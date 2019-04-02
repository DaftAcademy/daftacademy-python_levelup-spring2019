from uuid import uuid4

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from decorators import requires_basic_auth, requires_user_session
from errors import InvalidUsage
from utils import get_train_from_json


app = Flask(__name__)

# Good to know:
# python-decouple
# https://12factor.net/
app.secret_key = 'sekretnyklucz'
app.trains = {}


def set_train():
    train_id = str(uuid4())
    data = get_train_from_json()
    app.trains[train_id] = data
    return train_id


@app.route('/')
def root():
    return 'Hello, World!'


@app.route('/login', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect(url_for('hello'))


@app.route('/hello')
@requires_user_session
def hello():
    return render_template('greeting.html', name=session['username'])


@app.route('/logout', methods=['GET', 'POST'])
@requires_user_session
def logout():
    if request.method == 'GET':
        return redirect(url_for('root'))
    del session['username']
    return redirect(url_for('root'))


@app.route('/trains', methods=['GET', 'POST'])
@requires_user_session
def trains():
    if request.method == 'GET':
        return jsonify(app.trains)
    elif request.method == 'POST':
        train_id = set_train()
        return redirect(url_for('train', train_id=train_id, format='json'))


@app.route('/trains/<train_id>', methods=['GET', 'DELETE'])
@requires_user_session
def train(train_id):
    if train_id not in app.trains:
        return 'No such train', 404

    if request.method == 'DELETE':
        del app.trains[train_id]
        return '', 204

    if request.method == 'GET' and request.args.get('format') != 'json':
        raise InvalidUsage("Missing 'format=json' in query string.",
                           status_code=415)
    return jsonify(app.trains[train_id])


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False)
