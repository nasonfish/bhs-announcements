from announcements import db
from time import time
import datetime
from markdown import markdown
from hashlib import md5
from base64 import b64encode

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created = db.Column(db.Float)
    display = db.Column(db.Float)
    expire = db.Column(db.Float)
    archived = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, username, title, text, display, expire, archive=False):
        self.username = username
        self.title = title
        self.text = text
        self.created = time()
        self.display = display  # the time we start displaying the announcement
        self.expire = expire
        self.archived = archive
        db.session.add(self)
        db.session.commit()

    def get_display(self):
        return datetime.datetime.fromtimestamp(int(self.display)).strftime('%h %d at %l:%M %P')
    def get_created(self):
        return datetime.datetime.fromtimestamp(int(self.created)).strftime('%h %d at %l:%M %P')
    def get_expiry(self):
        return datetime.datetime.fromtimestamp(int(self.expire)).strftime('%h %d at %l:%M %P')

    def get_text(self):
        return markdown(self.text)

    def archive(self):
        self.archived = True

        db.session.add(self)
        db.session.commit()

class Password(db.Model):
    __tablename__ = "passwords"  # WHOOPDY DOO, DON'T MIND ME, JUST A PASSWORD TABLE OVER HERE MINDING MY OWN BUSINESS.
    password = db.Column(db.String(128), primary_key=True)

    def __init__(self, password):
        m = md5()
        m.update(password)
        self.password = b64encode(m.digest())

        db.session.add(self)
        db.session.commit()
