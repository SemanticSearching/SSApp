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
    SERVER = os.environ.get('SERVER') or "AWS"
    DOMAIN = os.environ.get('DOMAIN') or "semanticsearch.site"
    HOST = "localhost" if SERVER == "LOCAL" else DOMAIN
    HOST = os.environ.get("HOST") or "localhost"
    PATH_TO_FAISS = join(basedir, "db_storage/faiss_index.pickle")
    PATH_TO_DB = join(basedir, "db_storage/papers.db")
    PATH_TO_DB_FOLDER = join(basedir, "db_storage")
    PATH_TO_DOCXS = join(basedir, "static/docxs")
    PATH_TO_HTMLS = join(basedir, "static/htmls")
    PATH_TO_STATIC = join(basedir, "static")
    PATH_TO_TEMPLATES = join(basedir, "templates")
    DIRECTORY_TO_WATCH = join(basedir, "static/docxs")
    ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}
    PARSER_WIN = 3
    PARSER_MAX_WORDS = 100
    # dropzone variable
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = '.doc, .docx, .pdf'
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_TIMEOUT = None
