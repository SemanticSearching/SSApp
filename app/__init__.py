#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pysbd
from flask import Flask
from app.config import Config as cf
from flask_sqlalchemy import SQLAlchemy
from app.utils import load_bert_model, load_faiss_index
from flask_dropzone import Dropzone
from flask_login import LoginManager

app = Flask(__name__, static_folder=cf.PATH_TO_STATIC, template_folder=cf.PATH_TO_TEMPLATES)
app.config.from_object(cf)
db = SQLAlchemy(app)
dropzone = Dropzone(app)
login = LoginManager(app)
login.login_view = 'login'
sbd = pysbd.Segmenter(language="en", clean=False)
sent_bert = load_bert_model()


from app.parser_engine.database import gen_faiss, write_to_html, write_to_db
from app.models import User

if not os.path.exists(cf.PATH_TO_FAISS):
    if not os.path.exists(cf.PATH_TO_DB_FOLDER):
        os.mkdir(cf.PATH_TO_DB_FOLDER)
    db.create_all()
    u = User(username=cf.USERNAME)
    u.set_password(cf.PASSWORD)
    db.session.add(u)
    db.session.commit()
    gen_faiss(cf.PATH_TO_DB, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN,
              cf.PARSER_MAX_WORDS, cf.DOMAIN, None)
faiss_index = load_faiss_index(cf.PATH_TO_FAISS)

from app import routes, models






