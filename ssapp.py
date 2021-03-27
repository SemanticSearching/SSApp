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
from flask_sqlalchemy import SQLAlchemy
from parser_engine.monitor import Watcher
from threading import Thread

app = Flask(__name__, static_folder='static')
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}
app.config.from_object(Config)
db = SQLAlchemy(app)
dir_path = os.path.dirname(os.path.realpath(__file__))
seg = pysbd.Segmenter(language="en", clean=False)


monitor = Watcher()

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


def gen_link(title, sent):
    """
    given a sent, gen loc flag
    Args:
        title:
        sent:

    Returns:

    """
    # sents = seg.segment(sent)
    sents = sent.strip().split(" ")
    sent0 = sents[:2]
    sent2 = sents[-2:]
    # sent0 = sents[0].split(" ")
    # sent2 = sents[2].split(" ")
    prefix = "http://127.0.0.1:5000/static/htmls/{}.html#:~:text=".format(title)
    # prefix = "https://semanticsearch.site/static/htmls/{}.html#:~:text=".format(title)
    first, last = "", ""
    if len(sent0) > 2:
        sent0_len = 2
    else:
        sent0_len = len(sent0)
    if len(sent2) > 2:
        sent2_len = 2
    else:
        sent2_len = len(sent2)
    for i in range(sent0_len - 1):
        first += sent0[i]
        first += "%20"
    first += sent0[sent0_len - 1]
    for i in range(sent2_len - 1):
        last += sent2[i]
        last += "%20"
    last += sent2[sent2_len - 1]
    return prefix+first+","+last


model = load_bert_model()
if os.path.exists("./models/papers.pickle"):
    data = read_data()
    data = data.astype({"title": "string", "sent": "string", "id": "int"})
if os.path.exists("./models/faiss_index.pickle"):
    faiss_index = load_faiss_index()


@app.route('/')
def index():
    return render_template("searchpage.html")


@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':
        query = request.form['query'].strip()
        results = []
        if query:
            # Get paper IDs
            D, I = vector_search([query], model, faiss_index, 100)
            # Slice data on year
            # Get individual results
            for id_ in I.flatten().tolist():
                if id_ in data["id"].tolist():
                    f = data[(data.id == id_)]
                else:
                    continue
                title = f.iloc[0].title
                link = gen_link(f.iloc[0].title, f.iloc[0].sent)
                results.append((title, link))
    return render_template("results.html", results=results, in_q="{}".format(query))


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


