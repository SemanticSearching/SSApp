import pytest
import numpy as np
from pytest import approx
from app.utils import load_bert_model
from faiss import normalize_L2
from scipy import spatial
import os
from os.path import join
import shutil

model = load_bert_model()
cos_score = 0.4467635154724121
query = "afasdfsfsafsafafasdfafsfasfweftwerw2t2t"
result = "SAIC.vendor@am.jll.com"

query_embedding = model.encode([query])
normalize_L2(query_embedding)
result_embedding = model.encode([result])
normalize_L2(result_embedding)
cos_score_check = np.sum(query_embedding*result_embedding)
sos_score_scipy = 1 -spatial.distance.cosine(query_embedding, result_embedding)


def test_cos_score():
    assert cos_score_check == approx(cos_score)
    assert sos_score_scipy == approx(cos_score)


def test_rmdir():
    basedir = os.path.abspath(os.path.dirname(__file__))
    test_folder = join(basedir, "test_folder")
    os.mkdir(test_folder)
    with open(join(test_folder, "test.txt"), "w") as f:
        f.write("test")
    shutil.rmtree(test_folder)
    assert os.path.exists(test_folder) == False
