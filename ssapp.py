from flask import Flask, render_template, url_for, request, redirect, flash,\
    send_from_directory, current_app, send_from_directory
from werkzeug.utils import secure_filename
import faiss
import pickle
import pandas as pd
import os
import pysbd
from os.path import join
from sentence_transformers import SentenceTransformer
from vector_engine.utils import vector_search
from config import Config
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.sql.expression import case
# from parser_engine.tables import Paper
# from parser_engine.monitor import Watcher
from threading import Thread

app = Flask(__name__, static_folder='static')
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}
app.config.from_object(Config)
db = SQLAlchemy(app)
dir_path = os.path.dirname(os.path.realpath(__file__))
seg = pysbd.Segmenter(language="en", clean=False)
ROWS_PER_PAGE = 10
# monitor = Watcher()


class Paper(db.Model):
    title = db.Column(db.String(100), index=True)
    seg = db.Column(db.String(1000), index=True)
    link = db.Column(db.String(500), index=True)
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)

    def __repr__(self):
        return'<Paper {}>'.format(self.title)


def read_data(data="./models/papers.pickle"):
    """Read the data from pickle."""
    with open(data, "rb") as p:
        papers = pickle.load(p)
    return pd.DataFrame(data=papers, columns=["title", "sent", "id"])


def load_bert_model(name="distilbert-base-nli-stsb-mean-tokens"):
    """Instantiate a sentence-level DistilBERT model."""
    return SentenceTransformer(name)


def load_faiss_index(path_to_faiss = join(dir_path,
                                          "models/faiss_index.pickle")):
    """Load and deserialize the Faiss index."""
    with open(path_to_faiss, "rb") as h:
        data = pickle.load(h)
    return faiss.deserialize_index(data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


model = load_bert_model()
if os.path.exists("./models/papers.pickle"):
    data = read_data()
    data = data.astype({"title": "string", "sent": "string", "id": "int"})
if os.path.exists("./models/faiss_index.pickle"):
    faiss_index = load_faiss_index()


@app.route('/')
def index():
    return render_template("searchpage.html")


@app.route('/process', methods=["POST", "GET"])
def process():
    if request.method == 'POST':
        query_form = request.form['query'].strip()
        query_arg = ''
    else:
        query_arg = request.args.get('query').strip()
        query_form = ''
    query = query_form if query_form != '' else query_arg
    if query:
        # Get paper IDs
        D, I = vector_search([query], model, faiss_index, 100)
        ids = I.flatten().tolist()
        print(ids)
        ids_order = case({id: index for index, id in enumerate(ids)}, value=Paper.id)
        page = request.args.get('page', default=1, type=int)
        papers = Paper.query.filter(Paper.id.in_(ids)).order_by(ids_order).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("results.html", papers=papers, query_form=query_form, query_arg=query_arg)


@app.route('/document', methods=['GET', 'POST'])
def document():
    # return redirect(url_for('document', filename='document.html'))
    return render_template("document.html")


@app.route('/static/docs/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    doc_path = os.path.join(current_app.root_path, "static/docs")
    return send_from_directory(doc_path, filename=filename,
                               as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("searchpage.html")


if __name__ == '__main__':
    # monitor_thread = Thread(target=monitor.run())
    # monitor_thread.start()
    app.run(debug=True)
    # monitor_thread.join()


