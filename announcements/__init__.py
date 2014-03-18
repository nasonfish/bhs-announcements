from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('announcements.conf')
db = SQLAlchemy(app)

import announcements.models
import announcements.views


app.add_url_rule('/static/<path:filename>',
                 endpoint='static',
                 view_func=app.send_static_file)