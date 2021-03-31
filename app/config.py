import os
from os.path import join
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sampleeeeeeeeeee'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or join(basedir, 'static/docxs')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db_storage/papers.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # function variables
    ROWS_PER_PAGE = 10
    SERVER = "LOCAL"
    HOST = "127.0.0.1:5000" if SERVER == "LOCAL" else "semanticsearch.site"
    PATH_TO_FAISS = join(basedir, "db_storage/faiss_index.pickle")
    PATH_TO_DB = join(basedir, "db_storage/papers.db")
    PATH_TO_DB_FOLDER = join(basedir, "db_storage")
    PATH_TO_DOCXS = join(basedir, "static/docxs")
    PATH_TO_HTMLS = join(basedir, "static/htmls")
    PATH_TO_STATIC = join(basedir, "static")
    PATH_TO_TEMPLATES = join(basedir, "templates")
    ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}
    PARSER_WIN = 3
    PARSER_MAX_WORDS = 100
