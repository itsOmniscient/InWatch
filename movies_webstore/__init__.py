import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("CSRF_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'
db = SQLAlchemy(app)

from movies_webstore import routes
