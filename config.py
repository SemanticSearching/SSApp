import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Sampleeeeeeeeeee'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or './static/docxs'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'models/papers.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False