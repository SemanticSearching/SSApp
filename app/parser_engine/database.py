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
from pdf2docx import Converter
from tqdm import tqdm


def gen_faiss(path_to_papers: str, path_to_faiss: str, model, win_size: int
              = 3, max_words: int = 100):
    """
    gen faiss index at initialization
    Args:
        path_to_papers: path to papers.db
        path_to_faiss: path to faiss index
        model: sentence_bert model
        win_size: sliding window, default is 3
        max_words: max words per segment, default is 300

    Returns:
        None

    """
    # remove all the html in
    if os.path.exists(cf.PATH_TO_HTMLS):
        shutil.rmtree(cf.PATH_TO_HTMLS)
        os.mkdir(cf.PATH_TO_HTMLS)
    else:
        os.mkdir(cf.PATH_TO_HTMLS)
    # gen the faiss indexs
    doc_files = os.listdir(cf.PATH_TO_DOCXS)
    for i in tqdm(range(len(doc_files))):
        legal_name = doc_files[i].encode('utf-8', 'ignore').decode('utf-8')
        if legal_name != doc_files[i]:
            os.rename(join(cf.PATH_TO_DOCXS, doc_files[i]),
                      join(cf.PATH_TO_DOCXS, legal_name))
            print(f'non utf-8 characters in {legal_name} is removed')
        write_to_db(legal_name, path_to_papers, path_to_faiss, model,
                    win_size, max_words, None)


def gen_link(title, sent) -> str:
    """
    given a sent, gen url
    Args:
        title: doc title
        sent: segment

    Returns:
        gen percent encoded url

    """
    title_encode = urllib.parse.quote(title, safe='~()*!.\'')
    prefix = f"htmls/{title_encode}.html#:~:text="
    sent = sent.strip()
    return prefix + urllib.parse.quote(sent, safe='~()*!.\'')


def update_papers(title: str, sents: list, ids: list):
    """
    write to paper.db
    Args:
        title: title of doc
        sents: a list of segments
        ids: a list of ids

    Returns:
        none

    """
    for s, id in zip(sents, ids):
        link = gen_link(title, s)
        p = Paper(title=title, seg=s, link=link, id=id)
        db.session.add(p)
    db.session.commit()


def update_papers_index(embeddings: np.array, all_ids: list,
                        path_to_faiss: str, faissindex):
    """
    update the path_to_faiss.pickle file
    Args:
        embeddings: sentence_bert embeddings
        all_ids: ids
        path_to_faiss: path to faiss index pickle
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
    """
    convert doc to html
    Args:
        filepath: path of doc file

    Returns:
        none

    """
    newfile = os.path.basename(filepath)
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        html_path = os.path.join(cf.PATH_TO_HTMLS,
                                 newfile.replace(".docx", ".html"))
        with open(html_path, "a+", encoding="utf8") as f:
            f.write(html)
            print("new file %s is done" % newfile)


def write_to_db(file_name: str, path_to_papers: str, path_to_faiss: str,
                model, win_size: int, max_words: int, faissindex):
    """
    give one paper, update the papers.pickle and papers_index.pickle
    papers.pickle: np.array([title, sents, embedding, id])
    papers_index.pickle:
    Args:
        file_name: path of doc
        path_to_papers: path of paper.db
        path_to_faiss: path of faiss index pickle
        model: sentence_bert model
        win_size: sliding window size
        max_words: maximum words per segment
        faissindex: faiss index

    Returns:

    """
    if file_name.split(".")[-1] in cf.ALLOWED_EXTENSIONS:
        if file_name.split(".")[-1] == "pdf":
            doc_file_name = ".".join(file_name.split(".")[:-1]) + ".docx"
            cv = Converter(join(cf.PATH_TO_DOCXS, file_name))
            cv.convert(join(cf.PATH_TO_DOCXS, doc_file_name))
            cv.close()
            os.remove(join(cf.PATH_TO_DOCXS, file_name))
        else:
            doc_file_name = file_name
        title = ".".join(file_name.split(".")[:-1])
        if not os.path.exists(path_to_papers):
            db.create_all()
        latest_id = Paper.query.count()
        # Check if CUDA is available ans switch to GPU
        if torch.cuda.is_available():
            model = model.to(torch.device("cuda"))
        print(model.device)
        all_sents = docx_parser(join(cf.PATH_TO_DOCXS, doc_file_name),
                                sliding_window=win_size, max_words=max_words)
        all_ids = [int(i) for i in range(latest_id, latest_id + len(all_sents))]
        all_sents = [" ".join(segment) for segment in all_sents]
        # Convert abstracts to vectors
        embeddings = model.encode(all_sents, show_progress_bar=True)
        # change datatype
        embeddings = np.array([embedding for embedding in embeddings]).astype(
            "float32")
        update_papers(title, all_sents, all_ids)
        normalize_L2(embeddings)
        update_papers_index(embeddings, all_ids, path_to_faiss,
                            faissindex)
        write_to_html(join(cf.PATH_TO_DOCXS, doc_file_name))


if __name__ == '__main__':
    if not os.path.exists(cf.PATH_TO_FAISS):
        gen_faiss(cf.PATH_TO_HTMLS, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN,
                  cf.PARSER_MAX_WORDS)
