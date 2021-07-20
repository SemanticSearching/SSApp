#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pysbd
from flask import Flask
from app.config import Config as cf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.utils import load_bert_model, load_faiss_index
from flask_dropzone import Dropzone
from flask_login import LoginManager
import boto3

app = Flask(__name__, static_folder=cf.PATH_TO_STATIC, template_folder=cf.PATH_TO_TEMPLATES)
app.config.from_object(cf)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
dropzone = Dropzone(app)
login = LoginManager(app)
login.login_view = 'login'
sbd = pysbd.Segmenter(language="en", clean=False)
sent_bert = load_bert_model()


from app.parser_engine.database import gen_faiss, write_to_html, write_to_db
from app.models import User, Paper


with app.app_context():
    db.create_all()
login_user = User.query.filter_by(username=cf.USERNAME).first()
if not login_user:
    u = User(username=cf.USERNAME)
    u.set_password(cf.PASSWORD)
    db.session.add(u)
    db.session.commit()

# client = boto3.client('s3', aws_access_key_id = cf.ACCESS_KEY,
#                       aws_secret_access_key = cf.SECRET_ACCESS_KEY)

from app import routes, models






