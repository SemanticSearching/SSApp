import os
from os.path import join
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sampleeeeeeeeeee'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or join(basedir, 'static/docxs')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'db_storage/papers.db')
    # username, password, host, db_name
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:' + \
                              f'{DB_PASS}@' + f'{DB_HOST}/' + f'{DB_NAME}'
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # function variables
    ROWS_PER_PAGE = 10
    PATH_TO_FAISS = join(basedir, "db_storage/faiss_index.pickle")
    PATH_TO_DB = join(basedir, "db_storage/papers.db")
    PATH_TO_DB_FOLDER = join(basedir, "db_storage")
    PATH_TO_DOCXS = join(basedir, "static/docxs")
    PATH_TO_HTMLS = join(basedir, "static/htmls")
    PATH_TO_STATIC = join(basedir, "static")
    PATH_TO_TEMPLATES = join(basedir, "templates")
    DIRECTORY_TO_WATCH = join(basedir, "static/docxs")
    ALLOWED_EXTENSIONS = {'docx'}
    PARSER_WIN = 3
    PARSER_MAX_WORDS = 100
    # dropzone variable
    DROPZONE_MAX_FILE_SIZE = 10
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = '.docx'
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_TIMEOUT = None
    # faiss search engine parameters
    TOPK = 100
    THRESHOLD = 0.60
    SHOW_SCORE = False
    # User name and password
    USERNAME = os.environ.get("LOGIN_USER") or "parc"
    PASSWORD = os.environ.get("LOGIN_PASSWORD") or "sss"
    print(f"user name is: {USERNAME}, password is: {PASSWORD}")
    #
    APP_ADDR = os.environ.get("APP_ADDR") or "localhost"
