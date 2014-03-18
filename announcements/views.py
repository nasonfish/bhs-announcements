from announcements import app
from flask import render_template, redirect, request, url_for, abort
import datetime, time
from announcements.models import Post, Password
from hashlib import md5
from base64 import b64encode

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/submit/new', methods=['POST'])
def submit_post():
    if not request.form.get('password', False):
        print(request.form)
        abort(403)
    m = md5()
    m.update(request.form['password'])
    allow = Password.query.filter_by(password=b64encode(m.digest())).first()
    if not allow:
        print(allow)
        abort(403)
    archive = True if request.form.get('archive') else False
    if not archive:
        display = datetime.datetime.now()
        display += datetime.timedelta(days=int(request.form['display-day']))
        expiry = display
        expiry += datetime.timedelta(days=int(request.form['expiry']))
        display = display.strftime('%s')
        expiry = expiry.strftime('%s')
    else:
        display, expiry = time.time(), time.time()
    Post(request.form['username'], request.form['title'], request.form['text'],
         display, expiry, archive)
    return redirect(url_for('.submit'))

@app.route('/view')
def view():
    posts = Post.query.filter_by(deleted=False, archived=False).all()
    return render_template('view.html', posts=posts)

@app.route('/view/raw')
def raw():
    posts = Post.query.filter_by(deleted=False, archived=False).all()
    return render_template('view_raw.html', posts=posts)

@app.route('/edit', methods=['POST'])
def edit():
    pass

@app.route('/view/archive')
def archive():
    posts = Post.query.filter_by(deleted=False).all()
    return render_template('view_archive.html', posts=posts)