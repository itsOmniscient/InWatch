import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("CSRF_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yicdarshqphnbc:5d55d883b19400882160d1f9603b6d1435d8fcb098eab8def93691df99905f4f@ec2-54-217-195-234.eu-west-1.compute.amazonaws.com:5432/dfm9lrak34ac2o'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_route'

from movies_webstore import routes
