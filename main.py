import json
import uuid

from flask import Flask, render_template, redirect, url_for, session, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f4fd3b960ef03a8d03f2bdb12133201d35fe0481'


@app.route('/')
def main():
    is_login()
    config = open_config()
    return render_template('index.html', conf=config['satats'])


@app.route('/login')
def login():
    is_login()
    if session['login']:
        return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/reg')
def registration():
    is_login()
    if session['login']:
        return redirect(url_for('main'))
    return render_template('reg.html')


@app.route('/user_add')
def user_add():
    config = open_config()
    config['auth'].update({"login": request.form['login'], "passwd": request.form['passwd']})
    write_config(config)
    session['login'] = True
    return redirect(url_for('main'))


@app.route('/panel')
def admin_panel():
    config = open_config()
    is_login()
    if not session['login']:
        return redirect(url_for('main'))
    return render_template('panel.html', conf=config['satats'])


@app.route('/add_state', methods=['POST'])
def add_state():
    config = open_config()
    lastname = secure_filename(request.files['file'].filename).split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + lastname
    request.files['file'].save('static/imgs/' + filename)

    config['satats'].update({
        "satate_" + str(len(config['satats'])): {
            "titel": request.form['titel'],
            "img": filename,
            "text": request.form['text']
        }
    })
    write_config(config)
    return redirect(url_for('main'))


@app.route('/delete_state/<path:state>', methods=['POST'])
def delete_state(state):
    config = open_config()
    config['satate'].pop(state)
    write_config(config)
    return '200'


def is_login():
    if 'login' not in session:
        session['login'] = False


@app.route('/logged', methods=['POST'])
def logged():
    config = open_config()
    try:
        if config['auth']['login'] == request.form['login'] and config['auth']['passwd'] == request.form['passwd']:
            session['login'] = True
            return redirect(url_for('admin_panel'))
    except:
        print('fatal')
    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('main'))


def open_config() -> dict:
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)

    return config


def write_config(data):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)
