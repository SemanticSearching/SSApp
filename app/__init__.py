#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pysbd
from flask import Flask
from app.config import Config as cf
from flask_sqlalchemy import SQLAlchemy
from app.utils import load_bert_model, load_faiss_index
from flask_dropzone import Dropzone


app = Flask(__name__, static_folder=cf.PATH_TO_STATIC, template_folder=cf.PATH_TO_TEMPLATES)
app.config.from_object(cf)
db = SQLAlchemy(app)
dropzone = Dropzone(app)
sbd = pysbd.Segmenter(language="en", clean=False)
sent_bert = load_bert_model()


from app.parser_engine.database import gen_faiss, write_to_html, write_to_db

if not os.path.exists(cf.PATH_TO_FAISS):
    if not os.path.exists(cf.PATH_TO_DB_FOLDER):
        os.mkdir(cf.PATH_TO_DB_FOLDER)
    gen_faiss(cf.PATH_TO_DB, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN, cf.PARSER_MAX_WORDS, cf.SERVER, None)
faiss_index = load_faiss_index(cf.PATH_TO_FAISS)

from app import routes, models






