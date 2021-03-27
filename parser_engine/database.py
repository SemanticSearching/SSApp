# from ssapp import db
import pandas as pd

import torch
import os
import faiss
import pickle
import numpy as np
import pickle
import mammoth
from parser_engine.docx_parser import docx_parser


# class Paper(db.Model):
#     title = db.Column(db.String(500), primary_key=True)
#     seg = db.Column(db.String(1000), index=True)
#     embedding = db.Column(db.Integer, index=True, unique=True)
#
#     def __repr__(self):
#         return'<User {}>'.format(self.username)


def update_db():
    pass


def update_papers(contents, titles, sents, ids):
    arr = np.empty((0, 3))
    for t, s, i in zip(titles, sents, ids):
        sample = np.array([[t, s, int(i)]])
        arr = np.append(arr, sample, axis=0)
    papers = np.concatenate((contents, arr), axis=0)
    return papers


def update_papers_index(embeddings, all_ids, path_to_faiss):
    """
    update the path_to_faiss.pickle file
    Args:
        embeddings:
        all_ids:
        path_to_faiss:

    Returns:

    """
    if os.path.exists(path_to_faiss):
        with open(path_to_faiss, "rb") as h:
            indexs = pickle.load(h)
            indexs = faiss.deserialize_index(indexs)
    else:
        indexs = faiss.IndexFlatL2(embeddings.shape[1])
        indexs = faiss.IndexIDMap(indexs)
    indexs.add_with_ids(embeddings, np.array(all_ids))
    with open(path_to_faiss, "wb") as f_faiss:
        pickle.dump(faiss.serialize_index(indexs), f_faiss)
    print("update indexs done")


def write_to_html(filepath: str):
    newfile = os.path.basename(filepath)
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        html_path = os.path.join("../static/htmls", newfile.replace(".docx", ".html"))
        with open(html_path, "a+") as f:
            f.write(html)
            print("new file %s is done" % newfile)


def write_to_db(filepath: str, path_to_papers: str, path_to_faiss: str, model, win_size, max_words):
    """
    give one paper, update the papers.pickle and papers_index.pickle
    papers.pickle: np.array([title, sents, embedding, id])
    papers_index.pickle:
    Args:
        filepath:
        path_to_papers:
        path_to_faiss:
        model:

    Returns:

    """
    title = os.path.basename(filepath).strip(".docx")
    if os.path.exists(path_to_papers):
        with open(path_to_papers, "rb") as h:
            papers = pickle.load(h)
            latest_id = int(papers[-1, -1])
    else:
        # title, sents, embedding, id
        papers = np.empty((0, 3))
        latest_id = 0

    # Check if CUDA is available ans switch to GPU
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
    print(model.device)
    all_sents = docx_parser(filepath, sliding_window=win_size, max_words=max_words)
    all_ids = [int(i) for i in range(latest_id, latest_id+len(all_sents))]
    all_titles = [title for _ in range(len(all_sents))]
    #
    all_sents = [" ".join(segment) for segment in all_sents]
    # Convert abstracts to vectors
    embeddings = model.encode(all_sents, show_progress_bar=True)
    # change datatype
    embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
    papers = update_papers(papers, all_titles, all_sents, all_ids)
    with open(path_to_papers, "wb") as f_papers:
        pickle.dump(papers, f_papers)
    print("papers are stored in pickle")
    update_papers_index(embeddings, all_ids, path_to_faiss)


if __name__ == '__main__':
    write_to_db("test", ["content1", "content2", "content3"])
