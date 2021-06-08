import torch
import os
import faiss
from faiss import normalize_L2
import numpy as np
import pickle
import mammoth
from .docx_parser import docx_parser
from urllib.parse import quote_plus
from os.path import join
from app import db, sent_bert
from app.models import Paper
from app.config import Config as cf
import urllib
import shutil


def gen_faiss(path_to_papers, path_to_faiss, model, win_size, max_words, domain, faissindex):
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
        shutil.rmtree(cf.PATH_TO_HTMLS)
        os.mkdir(cf.PATH_TO_HTMLS)
    else:
        os.mkdir(cf.PATH_TO_HTMLS)
    # gen the faiss indexs
    doc_files = os.listdir(cf.PATH_TO_DOCXS)
    for doc in doc_files:
        filepath = join(cf.PATH_TO_DOCXS, doc)
        write_to_db(filepath, path_to_papers, path_to_faiss, model, win_size, max_words, domain, faissindex)
        write_to_html(filepath)


def gen_link(title, sent, domain):
    """
    given a sent, gen loc flag
    Args:
        title:
        sent:

    Returns:

    """
    title_encode = urllib.parse.quote(title, safe='~()*!.\'')
    prefix = f"{domain}/static/htmls/" + f"{title_encode}.html#:~:text="
    sent = sent.strip()
    return prefix + urllib.parse.quote(sent, safe='~()*!.\'')


def update_papers(title, sents, ids, domain):
    for s, id in zip(sents, ids):
        link = gen_link(title, s, domain)
        p = Paper(title=title, seg=s, link=link, id=id)
        db.session.add(p)
    db.session.commit()


def update_papers_index(embeddings, all_ids, path_to_faiss, faissindex):
    """
    update the path_to_faiss.pickle file
    Args:
        embeddings:
        all_ids:
        path_to_faiss:
    Returns:
    """
    if faissindex is not None:
        indexs = faissindex
    elif os.path.exists(path_to_faiss):
        with open(path_to_faiss, "rb") as h:
            indexs = pickle.load(h)
            indexs = faiss.deserialize_index(indexs)
    else:
        indexs = faiss.IndexFlatIP(embeddings.shape[1])
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
        with open(html_path, "a+", encoding="utf8") as f:
            f.write(html)
            print("new file %s is done" % newfile)


def write_to_db(filepath: str, path_to_papers: str, path_to_faiss: str, model, win_size:int, max_words:int, domain:str, faissindex):
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
    update_papers(title, all_sents, all_ids, domain)
    normalize_L2(embeddings)
    update_papers_index(embeddings, all_ids, path_to_faiss,
                        faissindex)


if __name__ == '__main__':
    if not os.path.exists(cf.PATH_TO_FAISS):
        gen_faiss(cf.PATH_TO_HTMLS, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN, cf.PARSER_MAX_WORDS)

