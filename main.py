from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f4fd3b960ef03a8d03f2bdb12133201d35fe0481'


@app.route('/')
def main():
    is_login()
    return render_template('index.html')


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


@app.route('/panel')
def admin_panel():
    is_login()
    if not session['login']:
        return redirect(url_for('main'))
    return render_template('panel.html')


def is_login():
    if 'login' not in session:
        session['login'] = False


@app.route('/logged')
def logged():
    session['login'] = True
    return redirect(url_for('admin_panel'))


@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
