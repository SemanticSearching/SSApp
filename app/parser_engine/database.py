import torch
import os
import faiss
import numpy as np
import pickle
import mammoth
from .docx_parser import docx_parser
from urllib.parse import quote_plus
from os.path import join
from app import db, sent_bert
from app.models import Paper
from app.config import Config as cf


def gen_faiss(path_to_papers, path_to_faiss, model, win_size, max_words):
    """

    Args:
        path_to_papers:
        path_to_faiss:
        model:
        win_size:
        max_words:

    Returns:

    """
    # remove all the html in
    if os.path.exists(cf.PATH_TO_HTMLS):
        os.rmdir(cf.PATH_TO_HTMLS)
        os.mkdir(cf.PATH_TO_HTMLS)
    else:
        os.mkdir(cf.PATH_TO_HTMLS)
    # gen the faiss indexs
    doc_files = os.listdir(cf.PATH_TO_DOCXS)
    for doc in doc_files:
        filepath = join(cf.PATH_TO_DOCXS, doc)
        write_to_db(filepath, path_to_papers, path_to_faiss, model, win_size, max_words)
        write_to_html(filepath)


def gen_link(title, sent, num=30):
    """
    given a sent, gen loc flag
    Args:
        title:
        sent:

    Returns:

    """
    prefix = "https://{}/static/htmls/" + "{}.html#:~:text=".format(title)
    sents = sent.strip().split(" ")
    if "" in sents:
        sents.remove("")
    if " " in sents:
        sents.remove(" ")
    if len(sents) < 2*num:
        # only first part
        first = quote_plus(sent.strip()).replace("+", "%20")
        return prefix + first
    else:
        # both first and last part
        first = quote_plus(" ".join(sents[:num])).replace("+", "%20")
        last = quote_plus(" ".join(sents[-num:])).replace("+", "%20")
        return prefix + first + "," + last


def update_papers(title, sents, ids):
    for s, id in zip(sents, ids):
        link = gen_link(title, s)
        p = Paper(title=title, seg=s, link=link, id=id)
        db.session.add(p)
    db.session.commit()


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
        html_path = os.path.join(cf.PATH_TO_HTMLS, newfile.replace(".docx", ".html"))
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
    if not os.path.exists(path_to_papers):
        db.create_all()
    latest_id = Paper.query.count()
    # Check if CUDA is available ans switch to GPU
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
    print(model.device)
    all_sents = docx_parser(filepath, sliding_window=win_size, max_words=max_words)
    all_ids = [int(i) for i in range(latest_id, latest_id+len(all_sents))]
    all_sents = [" ".join(segment) for segment in all_sents]
    # Convert abstracts to vectors
    embeddings = model.encode(all_sents, show_progress_bar=True)
    # change datatype
    embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
    update_papers(title, all_sents, all_ids)
    print("papers are stored in database")
    update_papers_index(embeddings, all_ids, path_to_faiss)


if __name__ == '__main__':
    if not os.path.exists(cf.PATH_TO_FAISS):
        gen_faiss(cf.PATH_TO_HTMLS, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN, cf.PARSER_MAX_WORDS)

