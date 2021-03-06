import sqlite3
from flask import Flask, url_for, render_template, flash, request, session, g, redirect, abort, json
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
    if request.args.get('order'):
        sort_order = request.args.get('order')
    else:
        sort_order = session.get('order')

    if sort_order == 'az':
        session['order'] = 'az'
        cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY title ASC')
    else:
        session['order'] = 'newest'
        cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY id DESC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
    return render_template('show_links.html', bookmarks=bookmarks)


@app.route('/az')
def az():
    session['order'] = 'az'
    cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY title ASC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
    return render_template('entries.html', bookmarks=bookmarks)


@app.route('/newest')
def newest():
    session['order'] = 'newest'
    cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY id DESC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
    return render_template('entries.html', bookmarks=bookmarks)


@app.route('/json')
def json_entries():
    cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY id DESC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
    return json.dumps(bookmarks)


@app.route('/json/az')
def az_json():
    cur = g.db.execute('SELECT title, link, note, id FROM bookmarks ORDER BY title ASC')
    bookmarks = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
    return json.dumps(bookmarks)


@app.route('/add', methods=['POST'])
def add_bookmark():
    if not session.get('logged_in'):
        abort(401)

    link = request.form['link']
    if link[:4] != 'http':
        link = 'http://' + link
    g.db.execute('INSERT INTO bookmarks(title, link, note) VALUES(?, ?, ?)', [request.form['title'], link, request.form['note']])
    g.db.commit()
    flash('New bookmark added')
    return redirect(url_for('show_entries'))


@app.route('/edit')
def edit_bookmark():
    if not session.get('logged_in'):
        abort(401)
    bookmark_id = request.args.get('id')

    if bookmark_id.isdigit():
        cur = g.db.execute('SELECT title, link, note, id FROM bookmarks WHERE id=?', [bookmark_id])
        bookmark = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
        return render_template('edit_link.html', bookmark=bookmark)
    else:
        flash("Error: can't find bookmark in database")
        return redirect(url_for('show_entries'))


@app.route('/save_edit', methods=['POST'])
def save_edit():
    if not session.get('logged_in'):
        abort(401)
    if request.form['id'].isdigit():
        g.db.execute('UPDATE bookmarks SET title=?, link=?, note=? WHERE id=?', ([request.form['title'], request.form['link'], request.form['note'], request.form['id']]))
        g.db.commit()
        flash('Updated bookmark')
        return redirect(url_for('show_entries'))
    else:
        flash("Error: can't save update")


@app.route('/delete')
def delete_bookmark():
    if not session.get('logged_in'):
        abort(401)
    bookmark_id = request.args.get('id')

    if bookmark_id.isdigit():
        cur = g.db.execute('SELECT title, link, note, id FROM bookmarks WHERE id=?', [bookmark_id])
        bookmark = [dict(title=row[0], link=row[1], note=row[2], id=row[3]) for row in cur.fetchall()]
        return render_template('delete_form.html', bookmark=bookmark)
    else:
        flash("Error: can't find bookmark in database")
        return redirect(url_for('show_entries'))


@app.route('/confirm_delete', methods=['POST'])
def confirm_delete():
    if not session.get('logged_in'):
        abort(401)
    if request.form['delete'] == 'delete':
        if request.form['id'].isdigit():
            g.db.execute('DELETE FROM bookmarks WHERE id=?', [request.form['id']])
            g.db.commit()
            flash('Deleted bookmark')
        else:
            flash("Error: can't save update")
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
