import sqlite3
from flask import Flask, url_for, render_template, flash, request, session, g, redirect, abort
from contextlib import closing

# config
DATABASE = 'bookmarks.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('SELECT title, link, note FROM bookmarks ORDER BY id DESC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2]) for row in cur.fetchall()]
    return render_template('show_links.html', bookmarks=bookmarks)


@app.route('/add', methods=['POST'])
def add_bookmark():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('INSERT INTO bookmarks(title, link, note) VALUES(?, ?, ?)',
        [request.form['title'], request.form['link'], request.form['note']])
    g.db.commit()
    flash('New bookmark added')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You have logged in! Hooray!')
            return redirect(url_for('show_entries'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
