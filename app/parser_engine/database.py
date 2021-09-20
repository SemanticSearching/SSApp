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
from io import BytesIO, StringIO


def gen_link(title, sent) -> str:
    """
    given a sent, gen url
    Args:
        title: doc title
        sent: segment

    Returns:
        gen percent encoded url

    """
    title = ".".join(title.split(".")[:-1])
    title_encode = urllib.parse.quote(title, safe='~()*!.\'')
    # title_encode = "+".join(title.split(" "))
    prefix = f"htmls/{title_encode}.html#:~:text="
    sent = sent.strip()
    return prefix + urllib.parse.quote(sent, safe='~()*!.\'')


def gen_faiss(s3, ssapp_docs, s3_bucket_name, paper_all, model, win_size: int=3,
              max_words: int=100):
    """
    gen faiss index at initialization
    Args:
        ssapp_docs: bucket
        paper_all: All papers in database
        model: sentence_bert model
        win_size: sliding window, default is 3
        max_words: max words per segment, default is 300

    Returns:
        None

    """
    # remove all the html in

    # gen the faiss indexs
    paper_titles = set([i.title for i in paper_all])
    faiss_indexs = None
    # if database has data, load the data into faiss_indexs
    if paper_all:
        paper_ids = np.array([i.id for i in paper_all])
        paper_embeddings = np.array([i.e1 + i.e2 + i.e3+ i.e4 for i in
                                     paper_all]).astype("float32")
        faiss_indexs = faiss.IndexFlatIP(paper_embeddings.shape[1])
        faiss_indexs = faiss.IndexIDMap(faiss_indexs)
        faiss_indexs.add_with_ids(paper_embeddings, paper_ids)
    for file in ssapp_docs.objects.filter(Prefix='docs/'):
        file_key = file.key
        if file_key.split('.')[-1] in cf.ALLOWED_EXTENSIONS:
            # if file name is not legal, rename aws s3 file name
            # legal_name has the format: docs/...
            legal_key = file_key.encode('utf-8', 'ignore').decode('utf-8')
            if legal_key != file_key:
                s3.Object(s3_bucket_name, legal_key).copy_from(
                    CopySource=f'{s3_bucket_name}/{file_key}')
                s3.Object(s3_bucket_name, file_key).delete()
            legal_name = legal_key[5:]
            if legal_name not in paper_titles:
                # write to db
                body = BytesIO(file.get()['Body'].read())
                faiss_indexs = write_to_db(legal_name, body, model, win_size,
                                           max_words, faiss_indexs)
                write_to_html(legal_name, body, s3, s3_bucket_name)
    return faiss_indexs


def update_papers(title: str, sents: list, embeddings, ids: list):
    """
    write to paper.db
    Args:
        title: title of doc
        sents: a list of segments
        ids: a list of ids

    Returns:
        none

    """
    for s, id, e in zip(sents, ids, embeddings):
        e = list(e)
        e1 = e[0: int(len(e)*0.25)]
        e2 = e[int(len(e)*0.25): int(len(e)*0.5)]
        e3 = e[int(len(e)*0.5): int(len(e)*0.75)]
        e4 = e[int(len(e)*0.75):]
        link = gen_link(title, s)
        p = Paper(title=title, link=link, seg=s, e1=e1, e2=e2, e3=e3, e4=e4,
                  id=id)
        db.session.add(p)
    db.session.commit()


def write_to_html(filename, body, s3, s3_bucket_name):
    """
    convert doc to html
    Args:
        filepath: path of doc file

    Returns:
        none

    """
    filename = filename.replace(".docx", ".html")
    result = mammoth.convert_to_html(body)
    html = result.value  # The generated HTML
    html_path = join(cf.PATH_TO_HTMLS, filename)
    with open(html_path, 'a+') as f:
        f.write(html)
    s3.meta.client.upload_file(html_path, s3_bucket_name, join('htmls', filename))
    os.remove(html_path)
    print('done')


def write_to_db(file_name: str, body, model, win_size: int,
                max_words: int, faiss_indexs):
    """
    give one paper, update the papers.pickle and papers_index.pickle
    papers.pickle: np.array([title, sents, embedding, id])
    papers_index.pickle:
    Args:
        file_name: path of doc
        model: sentence_bert model
        win_size: sliding window size
        max_words: maximum words per segment
        faiss_indexs: faiss index

    Returns:

    """
    latest_id = Paper.query.count()
    # Check if CUDA is available ans switch to GPU
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
    print(model.device)
    all_sents = docx_parser(body, sliding_window=win_size, max_words=max_words)
    all_ids = [int(i) for i in range(latest_id, latest_id + len(all_sents))]
    all_sents = [" ".join(segment) for segment in all_sents]
    # Convert abstracts to vectors
    embeddings = model.encode(all_sents, show_progress_bar=True)
    # change datatype
    embeddings = np.array([embedding for embedding in embeddings]).astype(
        "float32")
    normalize_L2(embeddings)
    update_papers(file_name, all_sents, embeddings.astype("float"), all_ids)
    if faiss_indexs:
        faiss_indexs.add_with_ids(embeddings, np.array(all_ids))
    else:
        faiss_indexs = faiss.IndexFlatIP(embeddings.shape[1])
        faiss_indexs = faiss.IndexIDMap(faiss_indexs)
        faiss_indexs.add_with_ids(embeddings, np.array(all_ids))
    return faiss_indexs


if __name__ == '__main__':
    if not os.path.exists(cf.PATH_TO_FAISS):
        gen_faiss(cf.PATH_TO_HTMLS, cf.PATH_TO_FAISS, sent_bert, cf.PARSER_WIN,
                  cf.PARSER_MAX_WORDS)
