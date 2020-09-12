from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Ignore the admin stuff for now, we won't use it at the moment.
admin = Admin(app, name="politiapp", template_mode='bootstrap3')

from app import models #Placed here so it isn't a circular import, since models tries to import db
#admin.add_view((ModelView(models.User, db.session)))

from app import routes #Placed here so it isn't a circular import, since routes imports app